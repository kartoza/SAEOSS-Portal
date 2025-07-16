import logging
from flask import request

from ckan.plugins import toolkit
from flask import Blueprint
from flask import jsonify
import ckan.model as model  # Correct import for model
import ckan.lib.munge as munge
import ckan.lib.helpers as h

logger = logging.getLogger(__name__)

thematic_blueprint = Blueprint(
    "thematic", __name__, template_folder="templates", url_prefix="/thematic"
)

@thematic_blueprint.route("/all/", methods=["GET"])
def get_all_thematic_groups():
    start = int(request.args.get("start", 0))
    limit = int(request.args.get("limit", 100))

    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user
    }

    data_dict = {
        'sort': 'metadata_modified desc'
    }

    try:
        result = toolkit.get_action('package_search')(context, data_dict)
        datasets = result['results']
        logger.debug(f"Found {len(datasets)} datasets")

        # Group datasets by topic_and_saeoss_themes -> iso_topic_category
        grouped = {}
        for ds in datasets:
            theme_list = ds.get('topic_and_saeoss_themes', [])
            if not theme_list or not isinstance(theme_list[0], dict):
                continue  # skip if no valid themes

            topic = theme_list[0].get('iso_topic_category')
            if not topic:
                continue  # skip if iso_topic_category is missing

            org_id = ds.get('organization', {}).get('id')
            org_image_url = None

            if org_id:
                try:
                    org = toolkit.get_action('organization_show')(context, {'id': org_id})
                    org_image_url = org.get('image_url')
                except Exception as e:
                    logger.warning(f"Could not fetch organization {org_id}: {e}")

            # Determine thumbnail URL
            image_url = ds.get('metadata_thumbnail') or org_image_url
            data_thumbnail = ""

            if image_url and not image_url.startswith('http'):
                #munge here should not have an effect only doing it incase
                #of potential vulnerability of dodgy api input
                image_url = munge.munge_filename_legacy(image_url)
                data_thumbnail = h.url_for_static(
                'uploads/group/%s' % image_url,
                qualified=True
                )
            else:
                data_thumbnail = image_url

            grouped.setdefault(topic, []).append({
                'title': ds.get('title'),
                'notes': ds.get('notes'),
                'name': ds.get('name'),
                'id': ds.get('id'),
                'organization': ds.get('organization', {}).get('title'),
                'metadata_modified': ds.get('metadata_modified'),
                'url': f"/dataset/{ds.get('name')}",
                'image_url': data_thumbnail
            })

        # Sort topic categories alphabetically
        sorted_grouped = dict(sorted(grouped.items()))

        return jsonify({
            "results": sorted_grouped
        })

    except toolkit.ObjectNotFound:
        return jsonify({"error": "No datasets found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
