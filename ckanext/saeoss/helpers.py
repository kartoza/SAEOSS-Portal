import json
import logging
import typing
import datetime
from urllib.parse import quote, urlparse, parse_qsl, urlencode
from html import escape as html_escape
from pathlib import Path
from shapely import geometry
from ckan import model
from .model.saved_search import SavedSearches
from ckan.plugins import toolkit
from ckan.lib.helpers import build_nav_main as core_build_nav_main
import ckan.lib.munge as munge
import ckan.lib.helpers as h

from ckan.logic import NotAuthorized

from . import constants
from .logic.action.saeoss import show_version

from ckan.common import c
from ckan.lib.dictization.model_dictize import package_dictize
from ckan.lib.dictization import table_dictize

logger = logging.getLogger(__name__)


# def get_saeoss_themes(*args, **kwargs) -> typing.List[typing.Dict[str, str]]:
#     logger.debug(f"inside get_saeoss_themes {args=} {kwargs=}")
#     try:
#         saeoss_themes = toolkit.get_action("tag_list")(
#             data_dict={"vocabulary_id": constants.SAEOSS_THEMES_VOCABULARY_NAME}
#         )
#     except toolkit.ObjectNotFound:
#         saeoss_themes = []
#     return [{"value": t, "label": t} for t in saeoss_themes]


def get_iso_topic_categories(*args, **kwargs) -> typing.List[typing.Dict[str, str]]:
    return [
        {"value": cat[0], "label": cat[1]} for cat in constants.ISO_TOPIC_CATEGORIES
    ]

def get_iso_topic_display(value) -> str:
    filtered_value = list(filter(lambda a: a[0] == value, constants.ISO_TOPIC_CATEGORIES))
    if filtered_value:
        return filtered_value[0][1]
    return ''

def get_default_spatial_search_extent(
        padding_degrees: typing.Optional[float] = None,
) -> typing.Dict:
    """
    Return GeoJSON polygon with bbox to use for default view of spatial search map widget.
    """
    configured_extent = toolkit.config.get(
        "ckan.saeoss.default_spatial_search_extent"
    )
    if padding_degrees and configured_extent:
        parsed_extent = json.loads(configured_extent)
        result = _pad_geospatial_extent(parsed_extent, padding_degrees)
    else:
        result = configured_extent
    return result


def get_default_bounding_box() -> typing.Optional[typing.List[float]]:
    """Return the default bounding box in the form upper left, lower right

    This function calculates the default bounding box from the
    `ckan.saeoss.default_spatial_search_extent` configuration value. Note that
    this configuration value is expected to be in GeoJSON format and in GeoJSON,
    coordinate pairs take the form `lon, lat`.

    This function outputs a list with upper left latitude, upper left latitude, lower
    right latitude, lower right longitude.

    """

    configured_extent = toolkit.config.get(
        "ckan.saeoss.default_spatial_search_extent"
    )
    parsed_extent = json.loads(configured_extent)
    return convert_geojson_to_bbox(parsed_extent)


def convert_geojson_to_bbox(
        geojson: typing.Dict,
) -> typing.Optional[typing.List[float]]:
    logger.error(geojson)
    if isinstance(geojson, str):
        try:
            geojson = json.loads(geojson)
        except json.decoder.JSONDecodeError:
            # bbox is already BBOX format
            # 5.0, 5.0, -1.7763568394002505e-15, 10.000000000000002
            return geojson.split(', ')
    try:
        coords = geojson["coordinates"][0]
    except TypeError:
        result = None
    else:
        min_lon = min(c[0] for c in coords)
        max_lon = max(c[0] for c in coords)
        min_lat = min(c[1] for c in coords)
        max_lat = max(c[1] for c in coords)
        result = [max_lat, min_lon, min_lat, max_lon]
    return result


def convert_string_extent_to_bbox(extent: str) -> typing.List[float]:
    if extent is None:
        return []
    coords_extent = []
    for value in extent.split(","):
        try:
            coords_extent.append(float(value))
        except ValueError:
            continue
    return coords_extent


def helper_show_version(*args, **kwargs) -> typing.Dict:
    return show_version()


def user_is_org_member(
        org_id: str, user=None, role: typing.Optional[str] = None
) -> bool:
    """Check if user has editor role in the input organization."""
    result = False
    if user is not None:
        member_list_action = toolkit.get_action("member_list")
        try:
            org_members = member_list_action(
                data_dict={"id": org_id, "object_type": "user"}
            )
        except:
            return result
        for member_id, _, member_role in org_members:
            if user.id == member_id:
                if role is None or member_role.lower() == role.lower():
                    result = True
                break
    return result


def org_member_list(org_id: str, role: typing.Optional[str] = None) -> typing.List:
    """Return list of organization members with the specified role"""
    member_list_action = toolkit.get_action("member_list")
    org_members = member_list_action(data_dict={"id": org_id, "object_type": "user"})

    results = []
    for member_id, _, member_role in org_members:
        if role is None or member_role.lower() == role.lower():
            results.append(member_id)

    return results


def user_is_staff_member(user_id: str) -> bool:
    """Check if user is a member of the staff org"""
    memberships_action = toolkit.get_action("organization_list_for_user")
    memberships = memberships_action(context={"user": user_id}, data_dict={})
    portal_staff = toolkit.config.get(
        "ckan.saeoss.portal_staff_organization_name", "saeoss staff"
    )
    for group in memberships:
        is_org = group.get("type", "organization") == "organization"
        is_portal_staff = group.get("title").lower() == portal_staff.lower()
        if is_org and is_portal_staff:
            result = True
            break
    else:
        result = False
    return result


def build_pages_nav_main(*args):
    """Reimplementation of ckanext-pages `build_pages_nav_main()`

    This function reimplements the original ckanext-pages in order to overcome
    a bug whereby the groups menu is not removable because of a typo in its route name.

    """

    about_menu = toolkit.asbool(toolkit.config.get("ckanext.pages.about_menu", True))
    group_menu = toolkit.asbool(toolkit.config.get("ckanext.pages.group_menu", True))
    org_menu = toolkit.asbool(
        toolkit.config.get("ckanext.pages.organization_menu", True)
    )

    new_args = []
    for arg in args:
        if arg[0] == "home.about" and not about_menu:
            continue
        if arg[0] == "organization.index" and not org_menu:
            continue
        if arg[0] == "group.index" and not group_menu:
            continue
        new_args.append(arg)

    output = core_build_nav_main(*new_args)

    # do not display any private pages in menu even for sysadmins
    pages_list = toolkit.get_action("ckanext_pages_list")(
        None, {"order": True, "private": False}
    )

    page_name = ""
    is_current_page = toolkit.get_endpoint() in (
        ("pages", "show"),
        ("pages", "blog_show"),
    )

    if is_current_page:
        page_name = toolkit.request.path.split("/")[-1]

    for page in pages_list:
        if page.get("title") == "About":
            continue  # nsif staff decided they don't want about page.
        type_ = "blog" if page["page_type"] == "blog" else "pages"
        name = quote(page["name"])
        title = html_escape(page["title"])
        link = toolkit.h.literal('<a href="/{}/{}">{}</a>'.format(type_, name, title))
        if page["name"] == page_name:
            li = (
                    toolkit.literal('<li class="active">') + link + toolkit.literal("</li>")
            )
        else:
            li = toolkit.literal("<li>") + link + toolkit.literal("</li>")
        output = output + li
    return output


def get_featured_datasets():
    search_action = toolkit.get_action("package_search")
    result = search_action(data_dict={"q": "featured:true", "rows": 5})
    return result["results"]


def get_featured_datasets_count():
    """
    used with facets count
    """
    search_action = toolkit.get_action("package_search")
    result = search_action(data_dict={"q": "featured:true", "include_private": True})
    return result["count"]


def get_recently_modified_datasets():
    search_action = toolkit.get_action("package_search")
    result = search_action(data_dict={"sort": "metadata_modified desc", "rows": 5})
    return result["results"]


def get_all_datasets_count(user_obj):
    """
    fixes a bug when applying
    solr active search

    """
    # context = {"user":c.user, "auth_user_obj":c.userobj}
    # return len(packages)
    # 32000 rows is the maximum of what can be retrieved
    # by ckan at once.
    # the question becomes, do i want you to know the private datasets count ?
    # q = """ select count(distinct(id)) from package where state='active' and type='dataset' """
    # result = model.Session.execute(q)
    # return result.fetchone()[0]

    # this doesn't work
    # results = toolkit.get_action("package_list")(context={"auth_user_obj": c.userobj}, data_dict={'include_private':True})

    result = toolkit.get_action("package_search")(
        data_dict={"q": "*:*", "include_private": True}
    )
    return result["count"]


def get_org_public_records_count(org_id: str) -> int:
    """
    the default behavior is showing fixed
    number of recoreds for orgs if the
    user is not a part of them in org
    list page, we are adjusting
    """
    query = model.Session.query(model.Package).filter(
        model.Package.owner_org == org_id,
        model.Package.private == "f",
        model.Package.state == "active",
        model.Package.type == "dataset",
    )
    count = len(query.all())
    return count


def get_datasets_thumbnail(data_dict):
    """
    Generate thumbnails based on metadataset
    """
    data_thumbnail = "/images/org.png"
    if data_dict.get("metadata_thumbnail"):
        data_thumbnail = data_dict.get("metadata_thumbnail")
    else:
        # data_resource = data_dict.get("resources")
        # for resource in data_resource:
        #     if resource["format"].lower() == "wms":
        #         wms_url = resource["url"]
        #         parsed_url = dict(parse_qsl(urlparse(wms_url).query))
        #         parsed_url["format"] = "image/png; mode=8bit"
        #         data_thumbnail = "%s?%s" % (
        #             wms_url.split("?")[0],
        #             urlencode(parsed_url),
        #         )
        #         break
        if 'organization' not in data_dict or not data_dict['organization']:
            return data_thumbnail
        image_url = data_dict['organization']['image_url']
        if image_url and not image_url.startswith('http'):
            #munge here should not have an effect only doing it incase
            #of potential vulnerability of dodgy api input
            image_url = munge.munge_filename_legacy(image_url)
            data_thumbnail = h.url_for_static(
            'uploads/group/%s' % data_dict['organization']['image_url'],
            qualified=True
            )
    return data_thumbnail


def _pad_geospatial_extent(extent: typing.Dict, padding: float) -> typing.Dict:
    geom = geometry.shape(extent)
    padded = geom.buffer(padding, join_style=geometry.JOIN_STYLE.mitre)
    oriented_padded = geometry.polygon.orient(padded)
    return geometry.mapping(oriented_padded)


def get_org_memberships(user_id: str):
    """Return a list of organizations and roles where the input user is a member"""
    query = (
        model.Session.query(model.Group, model.Member.capacity)
        .join(model.Member, model.Member.group_id == model.Group.id)
        .join(model.User, model.User.id == model.Member.table_id)
        .filter(
            model.User.id == user_id,
            model.Member.state == "active",
            model.Group.is_organization == True,
        )
        .order_by(model.Group.name)
    )
    return query.all()


def mod_scheming_flatten_subfield(subfield, data):
    """
    this is specifically for testing site
    and might not be useful after a while,
    we are mimicking and modifying
    https://github.com/ckan/ckanext-scheming/blob/master/ckanext/scheming/helpers.py#L414
    to avoid few errors
    """
    flat = dict(data)

    if subfield["field_name"] not in data:
        return flat

    for i, record in enumerate(data[subfield["field_name"]]):
        prefix = "{field_name}-{index}-".format(
            field_name=subfield["field_name"],
            index=i,
        )
        for k in record:
            """
            this is where the modification happens,
            records can be just an empty string,
            accessing it as a dict would cause a
            type error
            """
            if type(flat) is dict and type(record) is dict:
                flat[prefix + k] = record[k]
    return flat


def get_maintenance_custom_other_field_data(data_dict):
    """The custom field "maintenance" stores **other**
    options in an __extra structure in the database,
    in package_extra table, this structure
    doesn't show up with regular ckan actions like
    **package_show**, **package_search** ..etc., we need
    to grab it from the database, if other alternatives
    can be used (e.g. when using the pkg coming with
    /package/read.html, the whole data shows up)
    it would be preferable
    """
    dataset_id = data_dict.get("id")
    # will be none if we are creating new package
    if dataset_id is not None:
        q = f""" select value from package_extra where package_id='{data_dict["id"]}' AND key = 'maintenance_information'  """
        result = model.Session.execute(q)
        for row in result.fetchall():
            load_row = json.loads(dict(row)["value"])
            try:
                return load_row[0]["__extras"]["custom_other_choice_select"]
            except:
                pass

    # if package object (i.e found with /package/read.html) is used
    # keeping it for further solutions
    # dictized_data = data_dict.as_dict()
    # custom_other_choice_select= ""
    # try:
    #     maintenance_info = json.loads(dictized_data["extras"]["maintenance_information"])
    #     custom_other_choice_select = maintenance_info[0]["__extras"][
    #         "custom_other_choice_select"
    #     ]
    # except KeyError:
    #     pass
    # return custom_other_choice_select


def get_today_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_current_release():
    """get releases to website footer,
    the release depends on the environment,
    if it's staging it uses v*.*.*-rc, rather
    if it's production v.*.*.*
    """
    current_file_path = Path(__file__)
    releases_file_path = current_file_path.parent.joinpath("releases.txt")
    with open(releases_file_path) as f:
        releases = json.loads(f.read())
        current_branch = _get_git_branch()
        # this might change so main is release candidate
        # and release branch is the latest release
        if current_branch == "development":
            return releases.get("latest_release_candidate")
        elif current_branch == "main":
            return releases.get("latest_release")
        else:
            return ""


def _get_git_branch():
    """Getting the current branch name.

    """
    return "development"


def get_saved_searches():
    """Returns saved searches

    based on a user id.
    """
    if c.userobj is None:
        return []

    user_id = c.userobj.id
    if c.userobj.sysadmin:
        q = f""" select saved_search_title, search_query, saved_search_date, saved_search_id, owner_user from saved_searches order by owner_user """
    else:
        q = f""" select saved_search_title, search_query, saved_search_date, saved_search_id from saved_searches where owner_user='{user_id}' order by saved_search_date desc """
    rows = model.Session.execute(q)
    saved_searches_list = []
    for row in rows:
        saved_searches_list.append(row)
    # saved_searches_list = SavedSearches.get(SavedSearches,owner_user=user_id)
    return saved_searches_list


def get_user_name(user_id):
    """Get a user's username by its id

    :param
    user_id: User's id
    :type
    user_id:int
    """
    user_obj = model.Session.query(model.User).filter_by(id=user_id).first()
    return user_obj.name


def get_user_id(user_name: str):
    """Gets user id from its username (the username is also unique)

    :param
    user_name: User's username
    :type
    user_name:str
    """
    user_obj = model.Session.query(model.User).filter_by(name=user_name).first()
    return user_obj.id


def get_user_name_from_url(url: str):
    """Get user's name from url

    :param
    url: The url
    :type
    url:str
    """

    return url.split("/user/")[1]


def get_recent_news(number=5, exclude=None):
    """Get the five recent news.

    :param
    number: Number of new want to get
    :type
    number: int
    """
    news_list = toolkit.get_action("ckanext_pages_list")(
        None, {"order_publish_date": True, "private": False, "page_type": "news"}
    )
    new_list = []
    for news in news_list:
        if exclude and news["name"] == exclude:
            continue
        new_list.append(news)
        if len(new_list) == number:
            break

    return new_list


def get_seo_metatags(site_key):
    """Get metatags value for SEO.

    :param
    site_key: Site's key
    :type
    site_key: str
    """
    data_dict = {
        "site_author": toolkit.config.get(
            "ckan.site_author",
        ),
        "site_description": toolkit.config.get(
            "ckan.site_description",
        ),
        "site_keywords": toolkit.config.get(
            "ckan.site_keywords",
        ),
    }
    return data_dict[site_key]


def get_year():
    """Display current year in the footer.

    """
    return datetime.datetime.now().year


def get_user_dashboard_packages(user_id):
    """The current behavior displays
    all the available datasets to the
    user, we need only the datasets
    created by the user.

    :param
    user_id: User's id
    :type
    user_id: int
    """
    # q = f""" select package.*, key, value from package join package_extra on package_id=package.id where
    # package.creator_user_id='{user_id}' """ rows = model.Session.execute(q) packages = [] for row in rows:
    # packages.append(dict(row)) return packages
    query = model.Session.query(model.Package).filter(
        model.Package.creator_user_id == user_id
    )
    packages = [
        package_dictize(package, context={"user": user_id, "model": model})
        for package in query.all()
    ]
    return packages


def _get_reference_date(package_dict: typing.Dict) -> str:
    dataset_reference_date = None
    if 'extras' in package_dict:
        extras = [
            extra for extra in package_dict['extras'] if extra['key'] == 'dataset_reference_date'
        ]
        if extras:
            dataset_reference_dates = json.loads(extras[0]['value'])
            if dataset_reference_dates:
                dataset_reference_date = dataset_reference_dates[0]['reference']
    elif 'dataset_reference_date' in package_dict:
        dataset_reference_dates = package_dict['dataset_reference_date']
        if dataset_reference_dates:
            dataset_reference_date = dataset_reference_dates[0]['reference']
    return dataset_reference_date


def _get_tags(package_dict: typing.Dict) -> str:
    try:
        iso_category = get_iso_topic_display(package_dict['topic_and_saeoss_themes-0-iso_topic_category'])
    except KeyError:
        iso_category = get_iso_topic_display(package_dict['topic_and_saeoss_themes'][0]['iso_topic_category'])
    iso_category = iso_category.replace(', ', '-')
    # clean tag from any iso topic category
    tags = {
        tag['name'] for tag in package_dict['tags'] if
        tag['name'] not in [cat[1].replace(', ', '-') for cat in constants.ISO_TOPIC_CATEGORIES]
    }

    if iso_category:
        # add current iso topic category to tags
        tags.add(iso_category)
    return [{'name': tag, 'state': 'active'} for tag in tags]
