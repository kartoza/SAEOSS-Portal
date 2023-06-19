"""CKAN CLI commands for the saeoss extension"""

import datetime as dt
import inspect
import json
import logging
import os
import sys
import time
import traceback
import typing
from concurrent import futures
from pathlib import Path
import glob
from xml.dom.minidom import parse
import traceback
#import validators
import alembic.command
import alembic.config
import alembic.util.exc
import click
import ckan
import ckan.plugins as p
from ckan.plugins import toolkit
from ckan import model
from ckan.lib.navl import dictization_functions
from lxml import etree
from sqlalchemy import text as sla_text
from ckanext.harvest import utils as harvest_utils

from .. import provide_request_context

from .. import jobs
from ..email_notifications import get_and_send_notifications_for_all_users

from . import utils
from ._bootstrap_data import PORTAL_PAGES, SAEOSS_ORGANIZATIONS
from ._sample_datasets import (
    SAMPLE_DATASET_TAG,
    generate_sample_datasets,
)
from ._sample_organizations import SAMPLE_ORGANIZATIONS
from ._sample_users import SAMPLE_USERS
import xml.dom.minidom as dom
from ._cbers import (
    get_geometry,
    get_radiometric_resolution,
    get_projection,
    get_quality,
    get_dates,
    get_scene_path,
    get_scene_row,
    get_band_count,
    get_sensor_inclination,
    get_original_product_id,
    get_solar_azimuth_angle,
    get_spatial_resolution_x,
    get_spatial_resolution_y
)

from pystac_client import Client
from pystac import ItemCollection



logger = logging.getLogger(__name__)
_xml_parser = etree.XMLParser(resolve_entities=False)

_DEFAULT_LEGACY_SASDI_RECORD_DIR = (
        Path.home() / "data/storage/legacy_sasdi_downloader/csw_records"
)
_DEFAULT_LEGACY_SASDI_THUMBNAIL_DIR = (
        Path.home() / "data/storage/legacy_sasdi_downloader/thumbnails"
)
_DEFAULT_MAX_WORKERS = 5
_PYCSW_MATERIALIZED_VIEW_NAME = "public.saeoss_pycsw_view"


@click.group()
@click.option("--verbose", is_flag=True)
def saeoss(verbose: bool):
    """Commands related to the saeoss extension."""
    click_handler = utils.ClickLoggingHandler()
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO, handlers=(click_handler,)
    )


@saeoss.command()
def send_email_notifications():
    """Send pending email notifications to users

    This command should be ran periodically.

    """

    setting_key = "ckan.activity_streams_email_notifications"
    if toolkit.asbool(toolkit.config.get(setting_key)):
        env_sentinel = "CKAN_SMTP_PASSWORD"
        if os.getenv(env_sentinel) is not None:
            num_sent = get_and_send_notifications_for_all_users()
            logger.info(f"Sent {num_sent} emails")
            logger.info("Done!")
        else:
            logger.error(
                f"Could not find the {env_sentinel!r} environment variable. Email "
                f"notifications are not configured correctly. Aborting...",
            )
    else:
        logger.error(f"{setting_key} is not enabled in config. Aborting...")


@saeoss.group()
def bootstrap():
    """Bootstrap the saeoss extension"""


@saeoss.group()
def ingest():
    """ Ingest a collection to metadata"""


@saeoss.group()
def delete_data():
    """Delete saeoss bootstrapped and sample data"""


@saeoss.group()
def extra_commands():
    """Extra commands that are less relevant"""

@saeoss.group()
def stac():
    """Commnads related to STAC catalogues"""



# @saeoss.command()
@click.command()
def shell():
    """
    Launch a shell with CKAN already imported and ready to explore

    The implementation of this command is mostly inspired and adapted from django's
    `shell` command

    """

    try:
        from IPython import start_ipython

        start_ipython(argv=[])
    except ImportError:
        import code

        # Set up a dictionary to serve as the environment for the shell.
        imported_objects = {}

        # By default, this will set up readline to do tab completion and to read and
        # write history to the .python_history file, but this can be overridden by
        # $PYTHONSTARTUP or ~/.pythonrc.py.
        try:
            sys.__interactivehook__()
        except Exception:
            # Match the behavior of the cpython shell where an error in
            # sys.__interactivehook__ prints a warning and the exception and continues.
            print("Failed calling sys.__interactivehook__")
            traceback.print_exc()

        # Set up tab completion for objects imported by $PYTHONSTARTUP or
        # ~/.pythonrc.py.
        try:
            import readline
            import rlcompleter

            readline.set_completer(rlcompleter.Completer(imported_objects).complete)
        except ImportError:
            pass

        # Start the interactive interpreter.
        code.interact(local=imported_objects)


@bootstrap.command()
def create_pages():
    """Create default pages"""
    logger.info("Creating default pages...")
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    existing_pages = toolkit.get_action("ckanext_pages_list")(
        context=context, data_dict={}
    )
    existing_page_names = [p["name"] for p in existing_pages]
    for page in PORTAL_PAGES:
        if page.name not in existing_page_names:
            logger.info(f"Creating page {page.name!r}...")
            toolkit.get_action("ckanext_pages_update")(
                context=context, data_dict=page.to_data_dict()
            )
        else:
            logger.info(f"Page {page.name!r} already exists, skipping...")
    logger.info("Done!")


@delete_data.command()
def delete_pages():
    """Delete default pages"""
    logger.info("Deleting default pages...")
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    existing_pages = toolkit.get_action("ckanext_pages_list")(
        context=context, data_dict={}
    )
    existing_page_names = [p["name"] for p in existing_pages]
    for page in PORTAL_PAGES:
        if page.name in existing_page_names:
            logger.info(f"Deleting page {page.name!r}...")
            toolkit.get_action("ckanext_pages_delete")(
                context=context, data_dict={"page": page.name}
            )
        else:
            logger.info(f"Page {page.name!r} does not exist, skipping...")
    logger.info("Done!")


@bootstrap.command()
def create_saeoss_organizations():
    """Create main Saeoss organizations

    This command creates the main Saeoss organizations.

    This function may fail if the Saeoss organizations already exist but are disabled,
    which can happen if they are deleted using the CKAN web frontend.

    This is a product of a CKAN limitation whereby it is not possible to retrieve a
    list of organizations regardless of their status - it will only return those that
    are active.

    """

    existing_organizations = toolkit.get_action("organization_list")(
        context={},
        data_dict={
            "organizations": [org.name for org in SAEOSS_ORGANIZATIONS],
            "all_fields": False,
        },
    )
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    for org_details in SAEOSS_ORGANIZATIONS:
        if org_details.name not in existing_organizations:
            logger.info(f"Creating organization {org_details.name!r}...")
            try:
                toolkit.get_action("organization_create")(
                    context={
                        "user": user["name"],
                        "return_id_only": True,
                    },
                    data_dict={
                        "name": org_details.name,
                        "title": org_details.title,
                        "description": org_details.description,
                        "image_url": org_details.image_url,
                    },
                )
            except toolkit.ValidationError:
                logger.exception(f"Could not create organization {org_details.name!r}")
    logger.info("Done!")


@delete_data.command()
def delete_saeoss_organizations():
    """Delete the main Saeoss organizations.

    This command will delete the Saeoss organizations from the CKAN DB - CKAN refers to
    this as purging the organizations (the CKAN default behavior is to have the delete
    command simply disable the existing organizations, but keeping them in the DB).

    It can safely be called multiple times - it will only ever delete the
    organizations once.

    """

    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    for org_details in SAEOSS_ORGANIZATIONS:
        logger.info(f"Purging  organization {org_details.name!r}...")
        try:
            toolkit.get_action("organization_purge")(
                context={"user": user["name"]}, data_dict={"id": org_details.name}
            )
        except toolkit.ObjectNotFound:
            logger.info(
                f"Organization {org_details.name!r} does not exist, skipping..."
            )
    logger.info(f"Done!")


@saeoss.group()
def load_sample_data():
    """Load sample data into non-production deployments"""


@load_sample_data.command()
def create_sample_users():
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    create_user_action = toolkit.get_action("user_create")
    logger.info(f"Creating sample users ...")
    for user_details in SAMPLE_USERS:
        logger.debug(f"Creating {user_details.name!r}...")
        try:
            create_user_action(
                context={
                    "user": user["name"],
                },
                data_dict={
                    "name": user_details.name,
                    "email": user_details.email,
                    "password": user_details.password,
                },
            )
        except toolkit.ValidationError:
            logger.exception(f"Could not create user {user_details.name!r}")
            logger.debug("Attempting to re-enable possibly deleted user...")
            sample_user = model.User.get(user_details.name)
            if sample_user is None:
                logger.error(f"Could not find sample_user {user_details.name!r}")
                continue
            else:
                sample_user.undelete()
                model.repo.commit()


@load_sample_data.command()
@provide_request_context
def create_sample_organizations(app_context):
    """Create sample organizations and members"""
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    create_org_action = toolkit.get_action("organization_create")
    create_org_member_action = toolkit.get_action("organization_member_create")
    create_harvester_action = toolkit.get_action("harvest_source_create")
    logger.info(f"Creating sample organizations ...")
    for org_details, memberships, harvesters in SAMPLE_ORGANIZATIONS:
        logger.debug(f"Creating {org_details.name!r}...")
        try:
            create_org_action(
                context={
                    "user": user["name"],
                },
                data_dict={
                    "name": org_details.name,
                    "title": org_details.title,
                    "description": org_details.description,
                    "image_url": org_details.image_url,
                },
            )
        except toolkit.ValidationError:
            logger.exception(f"Could not create organization {org_details.name!r}")
        for user_name, role in memberships:
            logger.debug(f"Creating membership {user_name!r} ({role!r})...")
            create_org_member_action(
                context={
                    "user": user["name"],
                },
                data_dict={
                    "id": org_details.name,
                    "username": user_name,
                    "role": role if role != "publisher" else "admin",
                },
            )
        for harvester_details in harvesters:
            logger.debug(f"Creating harvest source {harvester_details.name!r}...")
            try:
                create_harvester_action(
                    context={"user": user["name"]},
                    data_dict={
                        "name": harvester_details.name,
                        "url": harvester_details.url,
                        "source_type": harvester_details.source_type,
                        "frequency": harvester_details.update_frequency,
                        "config": json.dumps(harvester_details.configuration),
                        "owner_org": org_details.name,
                    },
                )
            except toolkit.ValidationError:
                logger.exception(
                    f"Could not create harvest source {harvester_details.name!r}"
                )
                logger.debug(
                    f"Attempting to re-enable possibly deleted harvester source..."
                )
                sample_harvester = model.Package.get(harvester_details.name)
                if sample_harvester is None:
                    logger.error(
                        f"Could not find harvester source {harvester_details.name!r}"
                    )
                    continue
                else:
                    sample_harvester.state = model.State.ACTIVE
                    model.repo.commit()
    logger.info("Done!")


@delete_data.command()
def delete_sample_users():
    """Delete sample users."""
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    delete_user_action = toolkit.get_action("user_delete")
    logger.info(f"Deleting sample users ...")
    for user_details in SAMPLE_USERS:
        logger.info(f"Deleting {user_details.name!r}...")
        delete_user_action(
            context={"user": user["name"]},
            data_dict={"id": user_details.name},
        )
    logger.info("Done!")


@delete_data.command()
def delete_sample_organizations():
    """Delete sample organizations."""
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})

    org_show_action = toolkit.get_action("organization_show")
    purge_org_action = toolkit.get_action("organization_purge")
    package_search_action = toolkit.get_action("package_search")
    dataset_purge_action = toolkit.get_action("dataset_purge")
    harvest_source_list_action = toolkit.get_action("harvest_source_list")
    harvest_source_delete_action = toolkit.get_action("harvest_source_delete")
    logger.info(f"Purging sample organizations ...")
    for org_details, _, _ in SAMPLE_ORGANIZATIONS:
        try:
            org = org_show_action(
                context={"user": user["name"]}, data_dict={"id": org_details.name}
            )
            logger.debug(f"{org = }")
        except toolkit.ObjectNotFound:
            logger.info(f"Organization {org_details.name} does not exist, skipping...")
        else:
            packages = package_search_action(
                context={"user": user["name"]},
                data_dict={"fq": f"owner_org:{org['id']}"},
            )
            logger.debug(f"{packages = }")
            for package in packages["results"]:
                logger.debug(f"Purging package {package['id']}...")
                dataset_purge_action(
                    context={"user": user["name"]}, data_dict={"id": package["id"]}
                )
            harvest_sources = harvest_source_list_action(
                context={"user": user["name"]}, data_dict={"organization_id": org["id"]}
            )
            logger.debug(f"{ harvest_sources = }")
            for harvest_source in harvest_sources:
                logger.debug(f"Deleting harvest_source {harvest_source['title']}...")
                harvest_source_delete_action(
                    context={"user": user["name"], "clear_source": True},
                    data_dict={"id": harvest_source["id"]},
                )
            logger.debug(f"Purging {org_details.name!r}...")
            purge_org_action(
                context={"user": user["name"]},
                data_dict={"id": org["id"]},
            )
    logger.info("Done!")


@load_sample_data.command()
@click.argument("owner_org")
@click.option("-n", "--num-datasets", default=10, show_default=True)
@click.option("-p", "--name-prefix", default="sample-dataset", show_default=True)
@click.option("-s", "--name-suffix")
@click.option(
    "-t",
    "--temporal-range",
    nargs=2,
    type=click.DateTime(),
    default=(dt.datetime(2021, 1, 1), dt.datetime(2022, 12, 31)),
)
@click.option("-x", "--longitude-range", nargs=2, type=float, default=(16.3, 33.0))
@click.option("-y", "--latitude-range", nargs=2, type=float, default=(-35.0, -21.0))
def create_sample_datasets(
        owner_org,
        num_datasets,
        name_prefix,
        name_suffix,
        temporal_range,
        longitude_range,
        latitude_range,
):
    """Create multiple sample datasets"""
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    datasets = generate_sample_datasets(
        num_datasets,
        name_prefix,
        owner_org,
        name_suffix,
        temporal_range_start=temporal_range[0],
        temporal_range_end=temporal_range[1],
        longitude_range_start=longitude_range[0],
        longitude_range_end=longitude_range[1],
        latitude_range_start=latitude_range[0],
        latitude_range_end=latitude_range[1],
    )
    ready_to_create_datasets = [ds.to_data_dict() for ds in datasets]
    workers = min(3, len(ready_to_create_datasets))
    with futures.ThreadPoolExecutor(workers) as executor:
        to_do = []
        for dataset in ready_to_create_datasets:
            future = executor.submit(utils.create_single_dataset, user, dataset)
            to_do.append(future)
        num_created = 0
        num_already_exist = 0
        num_failed = 0
        for done_future in futures.as_completed(to_do):
            try:
                result = done_future.result()
                if result == utils.DatasetCreationResult.CREATED:
                    num_created += 1
                elif result == utils.DatasetCreationResult.NOT_CREATED_ALREADY_EXISTS:
                    num_already_exist += 1
            except dictization_functions.DataError:
                logger.exception(f"Could not create dataset")
                num_failed += 1
            except ValueError:
                logger.exception(f"Could not create dataset")
                num_failed += 1

    logger.info(f"Created {num_created} datasets")
    logger.info(f"Skipped {num_already_exist} datasets")
    logger.info(f"Failed to create {num_failed} datasets")
    logger.info("Done!")


# TODO: speed this up by doing concurrent processing, similar to create_sample_datasets
@delete_data.command()
def delete_sample_datasets():
    """Deletes at most 1000 of existing sample datasets"""
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    purge_dataset_action = toolkit.get_action("dataset_purge")
    get_datasets_action = toolkit.get_action("package_search")
    max_rows = 1000
    existing_sample_datasets = get_datasets_action(
        context={"user": user["name"]},
        data_dict={
            "q": f"tags:{SAMPLE_DATASET_TAG}",
            "rows": max_rows,
            "facet": False,
            "include_drafts": True,
            "include_private": True,
        },
    )
    for dataset in existing_sample_datasets["results"]:
        logger.debug(f"Purging dataset {dataset['name']!r}...")
        purge_dataset_action(
            context={"user": user["name"]}, data_dict={"id": dataset["id"]}
        )
    num_existing = existing_sample_datasets["count"]
    remaining_sample_datasets = num_existing - max_rows
    if remaining_sample_datasets > 0:
        logger.info(f"{remaining_sample_datasets} still remain")
    logger.info("Done!")


# TODO: This command does not need to be needed anymore,
#  since the vanilla ckan command seems to work - leaving t here in case we
#  eventually need it
@extra_commands.command()
@click.option("-m", "--message")
@click.option("-a", "--autogenerate", is_flag=True)
def add_db_revision(message, autogenerate):
    plugin_name = "saeoss"
    alembic_wrapper = AlembicWrapper(plugin_name)
    out = alembic_wrapper.run_command(
        alembic.command.revision,
        message=message,
        autogenerate=autogenerate,
        head=f"{plugin_name}@head",
        version_path=alembic_wrapper.version_path,
    )
    logger.info(f"{out=}")


@extra_commands.command()
@click.argument("alembic_command")
@click.option(
    "--collect-args",
    help="Should the command args be collected into a list?",
    is_flag=True,
)
@click.option(
    "--command-arg",
    multiple=True,
    help="Arguments for the alembic command. Can be provided multiple times",
)
@click.option(
    "--command-kwarg",
    multiple=True,
    help=(
            "Provide each keyword argument as a colon-separated string of "
            "key_name:value. This option can be provided multiple times"
    ),
)
def defer_to_alembic(alembic_command, collect_args, command_arg, command_kwarg):
    """Run an alembic command

    Examples:

        \b
        defer-to-alembic current --command-kwarg=verbose:true
        defer-to-alembic heads --command-kwarg=verbose:true
        defer-to-alembic history

    """

    alembic_wrapper = AlembicWrapper("saeoss")
    bool_keys = (
        "verbose",
        "autogenerate",
    )
    try:
        command = getattr(alembic.command, alembic_command)
    except AttributeError:
        logger.exception("Something wrong with retrieving the command")
    else:
        kwargs = {}
        for raw_kwarg in command_kwarg:
            key, value = raw_kwarg.partition(":")[::2]
            if key in bool_keys:
                kwargs[key] = toolkit.asbool(value)
            else:
                kwargs[key] = value
        if collect_args:
            out = alembic_wrapper.run_command(command, command_arg, **kwargs)
        else:
            out = alembic_wrapper.run_command(command, *command_arg, **kwargs)
        for line in out:
            logger.info(line)
        logger.info("Done!")


def _resolve_alembic_config(plugin):
    if plugin:
        plugin_obj = p.get_plugin(plugin)
        if plugin_obj is None:
            toolkit.error_shout("Plugin '{}' cannot be loaded.".format(plugin))
            raise click.Abort()
        plugin_dir = os.path.dirname(inspect.getsourcefile(type(plugin_obj)))

        # if there is `plugin` folder instead of single_file, find
        # plugin's parent dir
        ckanext_idx = plugin_dir.rfind("/ckanext/") + 9
        idx = plugin_dir.find("/", ckanext_idx)
        if ~idx:
            plugin_dir = plugin_dir[:idx]
        migration_dir = os.path.join(plugin_dir, "migration", plugin)
    else:
        import ckan.migration as _cm

        migration_dir = os.path.dirname(_cm.__file__)
    return os.path.join(migration_dir, "alembic.ini")


class AlembicWrapper:
    alembic_conf: alembic.config.Config
    _command_output: typing.List[str]
    _plugin_name: str

    def __init__(self, plugin_name):
        self._plugin_name = plugin_name
        self.alembic_conf = self._get_alembic_config(plugin_name)
        self._command_output = []

    @property
    def version_path(self):
        alembic_config_ini = Path(_resolve_alembic_config(self._plugin_name))
        return str(alembic_config_ini.parent / "versions")

    def run_command(self, alembic_command, *args, **kwargs):
        current_output_index = len(self._command_output)
        logger.debug(f"{args=}")
        logger.debug(f"{kwargs=}")
        alembic_command(self.alembic_conf, *args, **kwargs)
        return self._command_output[current_output_index:]

    def _capture_alembic_output(self, message: str, *args):
        message = message % args
        self._command_output.append(message)

    def _get_alembic_config(self, plugin_name: str):
        alembic_config_ini = Path(_resolve_alembic_config(plugin_name))
        ckan_versions_path = str(Path(ckan.__file__).parent / "migration/versions")
        if alembic_config_ini.exists():
            conf = alembic.config.Config(
                str(alembic_config_ini), ini_section=plugin_name
            )
            conf.set_main_option("script_location", str(alembic_config_ini.parent))
            conf.set_main_option("sqlalchemy.url", toolkit.config.get("sqlalchemy.url"))
            conf.set_main_option(
                "version_locations",
                " ".join((f"%(here)s/versions", ckan_versions_path)),
            )
            conf.print_stdout = self._capture_alembic_output
            logger.debug(
                f"version_locations in the config: "
                f"{conf.get_main_option('version_locations')}"
            )
        else:
            raise RuntimeError("Input plugin name does not have alembic config")
        return conf


@extra_commands.command()
@click.argument("job_name")
@click.option(
    "--job-arg",
    multiple=True,
    help="Arguments for the job function. Can be provided multiple times",
)
@click.option(
    "--job-kwarg",
    multiple=True,
    help=(
            "Provide each keyword argument as a colon-separated string of "
            "key_name:value. This option can be provided multiple times"
    ),
)
def test_background_job(job_name, job_arg, job_kwarg):
    """Run background jobs synchronously

    JOB_NAME is the name of the job function to be run. Look in the `jobs` module for
    existing functions.

    Example:

    \b
        ckan saeoss test-background-job \\
            notify_org_admins_of_dataset_maintenance_request \\
            --job-arg=f1733d0c-5188-43b3-8039-d95efb76b4f5

    """

    job_function = getattr(jobs, job_name, None)
    if job_function is not None:
        kwargs = {}
        for raw_kwarg in job_kwarg:
            key, value = raw_kwarg.partition(":")[::2]
            kwargs[key] = value
        job_function(*job_arg, **kwargs)
        logger.info("Done!")
    else:
        logger.error(f"Job function {job_name!r} does not exist")


@saeoss.group()
def pycsw():
    """Commands related to integration between CKAN and pycsw"""


@pycsw.command()
def create_materialized_view():
    """Create the materialized view used to map between CKAN and pycsw"""
    jinja_env = utils.get_jinja_env()
    template = jinja_env.get_template("pycsw/pycsw_view.sql")
    ddl_command = template.render(view_name=_PYCSW_MATERIALIZED_VIEW_NAME)
    with model.meta.engine.connect() as conn:
        conn.execute(sla_text(ddl_command))
        # conn.commit()
    logger.info("Done!")


@pycsw.command()
def refresh_materialized_view():
    """Refresh the materialized view used to map between CKAN and pycsw"""
    with model.meta.engine.connect() as conn:
        conn.execute(
            sla_text(
                f"REFRESH MATERIALIZED VIEW {_PYCSW_MATERIALIZED_VIEW_NAME} WITH DATA;"
            )
        )
    logger.info("Done!")


@pycsw.command()
def drop_materialized_view():
    """Delete the materialized view used to map between CKAN and pycsw"""
    with model.meta.engine.connect() as conn:
        conn.execute(
            sla_text(f"DROP MATERIALIZED VIEW {_PYCSW_MATERIALIZED_VIEW_NAME}")
        )
    logger.info("Done!")


@extra_commands.command()
@click.option(
    "--post-run-delay-seconds",
    help="How much time to sleep after performing the harvesting command",
    default=(60 * 5),
)
@click.pass_context
def harvesting_dispatcher(ctx, post_run_delay_seconds: int):
    """Manages the harvesting queue and then sleeps a while after that.

    This command takes care of submitting pending jobs and marking done jobs as finished.

    It is similar to ckanext.harvest's `harvester run` CLI command, with the difference
    being that this command is designed to run and then wait a specific amount of time
    before exiting. This is a workaround for the fact that it is not possible to
    specify a delay period when restarting docker containers in docker-compose's normal
    mode.

    NOTE: This command is not needed when running under k8s or docker-compose swarm
    mode, as these offer other ways to control periodic services. In that case you can
    simply configure the periodic service and then use

    `launch-ckan-cli harvester run`

    as the container's CMD instruction.

    """

    flask_app = ctx.meta["flask_app"]
    with flask_app.test_request_context():
        logger.info(f"Calling harvester run command...")
        harvest_utils.run_harvester()
    logger.info(f"Sleeping for {post_run_delay_seconds!r} seconds...")
    time.sleep(post_run_delay_seconds)
    logger.info("Done!")


@extra_commands.command()
@click.option(
    "--post-run-delay-seconds",
    help="How much time to sleep after refreshing the materialized view",
    default=(60 * 5),
)
@click.pass_context
def refresh_pycsw_materialized_view(ctx, post_run_delay_seconds: int):
    """Refreshes the pycsw materiolized view and then sleeps for a while

    This is similar to our own `ckan run pycsw refresh-materialized-view`, with the
    difference being that this command is designed to run and then wait a specific
    amount of time before exiting. This is a workaround for the fact that it is not
    possible to specify a delay period when restarting docker containers in
    docker-compose's normal mode.

    NOTE: This command is not needed when running under k8s or docker-compose swarm
    mode, as these offer other ways to control periodic services. In that case you can
    simply configure a periodic service and then use

    `launch-ckan-cli saeoss pycsw refresh-materizalied-view`

    as the container's CMD instruction.

    """

    flask_app = ctx.meta["flask_app"]
    with flask_app.test_request_context():
        logger.info(f"Calling the pycsw refresh-materialized-view command...")
        ctx.invoke(refresh_materialized_view)
    logger.info(f"Sleeping for {post_run_delay_seconds!r} seconds...")
    time.sleep(post_run_delay_seconds)
    logger.info("Done!")


@ingest.command()
@click.option(
    "--source-path",
    help="A path where CBERS xml source locate",
)
@click.option(
    "--user",
    help="user added the dataset",
)
def cbers(source_path,
          user,
          test_only_flag=True,
          verbosity_level=2,
          halt_on_error_flag=True,
          ):
    """
        Ingest a collection of CBERS metadata folders.

        :param test_only_flag: Whether to do a dummy run ( database will not be
            updated. Default False.
        :type test_only_flag: bool

        :param source_path: A CBERS created CBERS 04 metadata xml file and thumbnail.
        :type source_path: str

        :param verbosity_level: How verbose the logging output should be. 0-2
            where 2 is very very very very verbose! Default is 1.
        :type verbosity_level: int

        :param halt_on_error_flag: Whather we should stop processing when the first
            error is encountered. Default is True.
        :type halt_on_error_flag: bool

        :param ignore_missing_thumbs: Whether we should raise an error
            if we find we are missing a thumbnails. Default is False.
        :type ignore_missing_thumbs: bool
        """

    def log_message(message, level=1):
        """Log a message for a given leven.

        :param message: A message.
        :param level: A log level.
        """
        if verbosity_level >= level:
            print(message)

    log_message((
                    'Running CBERS 04 Importer with these options:\n'
                    'Test Only Flag: %s\n'
                    'Source Dir: %s\n'
                    'Verbosity Level: %s\n'
                    'Halt on error: %s\n'
                    '------------------')
                % (test_only_flag, source_path, verbosity_level,
                   halt_on_error_flag), 2)

    # Scan the source folder and look for any sub-folders
    # The sub-folder names should be e.g.
    # L5-_TM-_HRF_SAM-_0176_00_0078_00_920606_080254_L0Ra_UTM34S
    log_message('Scanning folders in %s' % source_path, 1)
    # Loop through each folder found

    ingestor_version = 'CBERS 04 ingestor version 1.1'
    record_count = 0
    updated_record_count = 0
    created_record_count = 0
    failed_record_count = 0
    log_message('Starting directory scan...', 2)
    list_dataset = glob.glob(os.path.join(source_path, '*.XML'))
    # workers = len(list_dataset)
    with futures.ThreadPoolExecutor(3) as executor:
        to_do = []
        for cbers_folder in list_dataset:
            record_count += 1

            try:
                # Get the folder name
                product_folder = os.path.split(cbers_folder)[-1]
                log_message(product_folder, 2)

                # Find the first and only xml file in the folder
                # search_path = os.path.join(str(cbers_folder), '*.XML')
                log_message(cbers_folder, 2)
                xml_file = glob.glob(cbers_folder)[0]
                file = os.path.basename(xml_file)
                file_name = os.path.splitext(file)[0]
                original_product_id = get_original_product_id(file_name)

                # Create a DOM document from the file
                dom = parse(xml_file)

                # First grab all the generic properties that any CBERS will have...
                geometry = get_geometry(log_message, dom)
                start_date_time, center_date_time = get_dates(
                    log_message, dom)
                # projection for GenericProduct
                projection = get_projection(dom)

                # Band count for GenericImageryProduct
                band_count = get_band_count(dom)
                row = get_scene_row(dom)
                path = get_scene_path(dom)
                solar_azimuth_angle = get_solar_azimuth_angle(dom)
                sensor_inclination = get_sensor_inclination()
                # # Spatial resolution x for GenericImageryProduct
                spatial_resolution_x = float(get_spatial_resolution_x(dom))
                # # Spatial resolution y for GenericImageryProduct
                spatial_resolution_y = float(
                    get_spatial_resolution_y(dom))
                log_message('Spatial resolution y: %s' % spatial_resolution_y, 2)

                # # Spatial resolution for GenericImageryProduct calculated as (x+y)/2
                spatial_resolution = (spatial_resolution_x + spatial_resolution_y) / 2
                log_message('Spatial resolution: %s' % spatial_resolution, 2)
                radiometric_resolution = get_radiometric_resolution(dom)
                log_message('Radiometric resolution: %s' % radiometric_resolution, 2)
                quality = get_quality(dom)
                # ProductProfile for OpticalProduct
                # product_profile = get_product_profile(log_message, original_product_id)

                # Do the ingestion here...

                data = {
                    'title': original_product_id,
                    'owner_org': '',
                    'spatial': geometry,
                    'spatial_representation_type': '007',
                    'spatial_reference_system': projection,
                    'reference': center_date_time,
                    'reference_date_type': '001',
                    'equivalent_scale': radiometric_resolution,
                    'name': 'SANSA',
                    'version': '1.0',
                    'radiometric_resolution': radiometric_resolution,
                    'band_count': band_count,
                    'unique_product_id': original_product_id,
                    'spatial_resolution_x': spatial_resolution_x,
                    'spatial_resolution_y': spatial_resolution_y,
                    'spatial_resolution': spatial_resolution,
                    'product_acquisition_start': start_date_time,
                    'sensor_inclination_angle': sensor_inclination,
                    'solar_azimuth_angle': solar_azimuth_angle,
                    'row': row,
                    'path': path,
                    'quality': quality
                }
                data["id"] = data["unique_product_id"]
                data["lineage"] = data["path"]
                data["notes"] = data["radiometric_resolution"]
                data["owner_org"] = 'sample-org-1'
                data["spatial"] = [
                [16.4699, -34.8212],
                [32.8931, -34.8212],
                [32.8931, -22.1265],
                [16.4699, -22.1265],
                [16.4699, -34.8212]
            ]

                logger.debug('catalogue=======> just after', str(data))

                # Check if it's already in catalogue:
                # try:
                #     today = datetime.today()
                #     time_stamp = today.strftime("%Y-%m-%d")
                #     log_message('Time Stamp: %s' % time_stamp, 2)
                # except Exception as e:
                #     print(e.message)

                # update_mode = True

            except Exception as e:
                log_message('Error on dataset value')

            logger.debug('catalogue=======>', str(data))
            user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {'name': user})
            future = executor.submit(utils.create_single_dataset, user, data)
            to_do.append(future)
            num_created = 0
            num_already_exist = 0
            num_failed = 0
            for done_future in futures.as_completed(to_do):
                try:
                    result = done_future.result()
                    if result == utils.DatasetCreationResult.CREATED:
                        num_created += 1
                    elif result == utils.DatasetCreationResult.NOT_CREATED_ALREADY_EXISTS:
                        num_already_exist += 1
                except dictization_functions.DataError:
                    logger.exception(f"Could not create dataset")
                    num_failed += 1
                except ValueError:
                    logger.exception(f"Could not create dataset")
                    num_failed += 1

    # To decide: should we remove ingested product folders?

    print('===============================')
    print('Products processed : %s ' % record_count)
    print('Products updated : %s ' % updated_record_count)
    print('Products imported : %s ' % created_record_count)
    print('Products failed to import : %s ' % failed_record_count)
    print('===============================')

@stac.command()
@click.option(
    "--url",
    help="url of the catalogue",
)
@click.option(
    "--user",
    help="auhtorized user name to create the dataset",
)
@click.option(
    "--max",
    help="maximum number of stac items to create datasets from",
)
def create_stac_dataset(user, url, max=10):
    """
    fetch data from a valid stac catalog
    and create datasets out of stack items
    
    :param user: authorized user name to create the dataset
    :type user: str
    
    :param url: url of the catalogue
    :type url: str

    todo:
    1. enchance the resources preview
    2. remove the filler data
    3. add proper checks for params (user, url, max)
    """
    # following url is used for tests
    #catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    # pattern = "^https:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+$"
    catalog = Client.open(url)
    collection1 = list(catalog.get_collections())[0]
    collection_items = collection1.get_items()
    data_dict = {}
    # if not validators.parse(url):
    #     logger.info("url is not valid, exiting")
    #     return
    
    try:
        max = int(max)
    except:
        max = 10
        logger.info("max is not an integer, setting it to 10")
    
    for i in range(max+1):
        item1 = next(collection_items)
        data_dict["id"] = catalog.id + item1.id
        data_dict["title"] = item1.id
        data_dict["name"] = item1.id
        # there might or might not be notes, let's take the notes of the catalog for the moment
        data_dict["notes"] = catalog.description
        data_dict["responsible_party-0-individual_name"] = "responsible individual name"
        data_dict["responsible_party-0-role"] = "owner"
        data_dict["responsible_party-0-position_name"] = "position name"
        data_dict["dataset_reference_date-0-reference"] = "2022-1-5"
        data_dict["dataset_reference_date-0-reference_date_type"] = "001"
        data_dict["topic_and_sasdi_theme-0-iso_topic_category"] = "farming"
        data_dict["owner_org"] = "kartoza"
        data_dict["private"] = False
        data_dict["metadata_language_and_character_set-0-dataset_language"] = "en"
        data_dict["metadata_language_and_character_set-0-metadata_language"] = "en"
        data_dict["metadata_language_and_character_set-0-dataset_character_set"] = "utf-8"
        data_dict["metadata_language_and_character_set-0-metadata_character_set"] = "utf-8"
        data_dict["lineage"] = "lineage statement"
        data_dict["distribution_format-0-name"] = "distribution format"
        data_dict["distribution_format-0-version"] = "1.0"
        data_dict["spatial"] = item1.bbox
        data_dict["spatial_parameters-0-equivalent_scale"] = "equivalent scale"
        data_dict["spatial_parameters-0-spatial_representation_type"] = "001"
        data_dict["spatial_parameters-0-spatial_reference_system"] = "EPSG:3456"
        data_dict["metadata_date"] = "metadata"
        data_dict["resources"] = []
        for link in item1.links:
            if link.rel == "thumbnail":
                data_dict["resources"].append({"name":link.target,"url":link.target, "format": "jpg", "format_version": "1.0"})

        with futures.ThreadPoolExecutor(3) as executor:

            user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {'name': user})
            logger.debug('stac_item:', str(data_dict))
            future = executor.submit(utils.create_single_dataset, user, data_dict)
            logger.debug(future.result())
