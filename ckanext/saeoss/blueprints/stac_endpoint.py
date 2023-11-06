# -*- coding: utf-8 -*-
"""
A blueprint rendering stac endpoint page.
"""
import json
import logging

import pandas as pd

from ckan import model
from ckan.common import c
from ckan.plugins import toolkit
from flask import Blueprint, request
import os
import json
import rasterio
import urllib.request
import pystac
from pystac.extensions.eo import Band, EOExtension
from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from tempfile import TemporaryDirectory
from shapely.geometry import shape
import ckan.plugins as p
from ckan import model
from flask import jsonify, Response

logger = logging.getLogger(__name__)


stac_api_blueprint = Blueprint(
    "stac_api", __name__, template_folder="templates", url_prefix="/stac"
)

def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)

    return [(min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))]

def get_bbox_and_footprint(raster):
    with rasterio.open(raster) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon([
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom]
        ])

        return (bbox, mapping(footprint))

@stac_api_blueprint.route("/catalog", methods = ['POST', 'GET'])
def catalog():
    """A blueprint rendering stac collection.
    """

    catalog = pystac.Catalog(id='catalog', 
                            description='This Catalog is an overview of data hosted on SAEOSS Web Portal.')

    package_list = p.toolkit.get_action("package_list")({},{})
    for package in package_list:
        package_dict = p.toolkit.get_action("package_show")({"model": model},{'id': package})
        package_spatial = json.loads(package_dict['spatial'])
        package_name = package_dict["name"]
        package_title = package_dict["title"]
        package_description = package_dict["notes"]
        resources = package_dict["resources"]
        package_date = package_dict["reference_date"]

        spatial_extent = pystac.SpatialExtent(bboxes=[bounding_box(package_spatial['coordinates'][0])])

        date_format = '%m/%d/%Y %H:%M:%S.%f'
        collection_interval = [pd.to_datetime(package_date, infer_datetime_format=True), datetime.now()]
        temporal_extent = pystac.TemporalExtent(intervals=[collection_interval])

        collection_extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)

        collection = pystac.Collection(id=package_title,
                                description=package_description,
                                extent=collection_extent,
                                license='',
                                href=f'http://localhost:5000/stac/collection/{package_name}')

        logger.debug(f"collection {json.dumps(collection.to_dict())}")

        catalog.add_child(collection)

    return json.dumps(catalog.to_dict(), indent=4)

@stac_api_blueprint.route("/collections", methods = ['POST', 'GET'])
def collection():

    collection_arr = []

    package_list = p.toolkit.get_action("package_list")({},{})
    for package in package_list:
        package_dict = p.toolkit.get_action("package_show")({"model": model},{'id': package})
        package_spatial = json.loads(package_dict['spatial'])
        package_name = package_dict["name"]
        package_title = package_dict["title"]
        package_description = package_dict["notes"]
        resources = package_dict["resources"]
        package_date = package_dict["reference_date"]

        spatial_extent = pystac.SpatialExtent(bboxes=[bounding_box(package_spatial['coordinates'][0])])

        collection_interval = [pd.to_datetime(package_date, infer_datetime_format=True), None]
        temporal_extent = pystac.TemporalExtent(intervals=[collection_interval])

        collection_extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)

        collection = pystac.Collection(id=package_title,
                                description=package_description,
                                extent=collection_extent,
                                license='',
                                href=f'http://localhost:5000/stac/collection/{package_name}')
        
        collection.add_link(pystac.Link.canonical(f"http://localhost:5000/dataset/{package_name}"))

        logger.debug(f"collection {json.dumps(collection.to_dict())}")

        collection_arr.append(collection.to_dict())

    return jsonify(collection_arr)


@stac_api_blueprint.route("/collection/<package_name>", methods = ['POST', 'GET'])
def featurecollection(package_name):

    package_dict = p.toolkit.get_action("package_show")({"model": model},{'id': package_name})
    logger.debug(f"package {package_dict}")
    package_spatial = json.loads(package_dict['spatial'])
    package_name = package_dict["name"]
    package_title = package_dict["title"]
    package_description = package_dict["notes"]
    resources = package_dict["resources"]
    package_date = package_dict["reference_date"]

    spatial_extent = pystac.SpatialExtent(bboxes=[bounding_box(package_spatial['coordinates'][0])])

    date_format = '%m/%d/%Y %H:%M:%S.%f'
    collection_interval = [pd.to_datetime(package_date, infer_datetime_format=True), datetime.now()]
    temporal_extent = pystac.TemporalExtent(intervals=[collection_interval])

    collection_extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)

    items = []
    
    for resource in resources:
        resource_id = resource["id"]
        resource_name = resource["name"]
        resource_url = resource["url"]
        resource_url_type = resource["url_type"]
        resource_format = resource["format"]
        # resource_description = resource["description"]
        resource_created = resource["created"]
        mimetype = resource["mimetype"]
        is_tiff = False
        if mimetype == 'image/tiff' and resource_url_type == 'upload':
            is_tiff = True
            first_folder = resource_id[0:3]
            second_folder = resource_id[3:6]
            file_name = resource_id[6:len(resource_id)]
            img_path = f"/home/appuser/data/resources/{first_folder}/{second_folder}/{file_name}"
            bbox, footprint = get_bbox_and_footprint(img_path)
        else:
            bbox = bounding_box(package_spatial['coordinates'][0])
            footprint = package_spatial

        collection_item = pystac.Item(id=f"{resource_name}_{resource_id}",
                               geometry=footprint,
                               bbox=bbox,
                               datetime=pd.to_datetime(resource_created, infer_datetime_format=True),
                               properties={},)
        
        if is_tiff:
            collection_item.add_asset(
                key='image',
                asset=pystac.Asset(
                    href=resource_url,
                    media_type=pystac.MediaType.GEOTIFF
                )
            )
        collection_item.add_links([
            pystac.Link.root(f"http://localhost:5000/stac/{package_name}/item/{resource_id}"),
            pystac.Link.canonical(f"http://localhost:5000/dataset/{package_name}/resource/{resource_id}")
        ])
        items.append(collection_item)
    collection = pystac.ItemCollection(items)
    
    return jsonify(collection.to_dict())   

@stac_api_blueprint.route("<package_name>/item/<item>", methods = ['POST', 'GET'])
def item(package_name, item):
    
    resource_dict = p.toolkit.get_action("resource_show")({"model": model},{'id': item})
    package_dict = package_dict = p.toolkit.get_action("package_show")({"model": model},{'id': package_name})

    package_spatial = json.loads(package_dict['spatial'])

    resource_id = resource_dict["id"]
    resource_name = resource_dict["name"]
    resource_url = resource_dict["url"]
    resource_url_type = resource_dict["url_type"]
    resource_format = resource_dict["format"]
    # resource_description = resource_dict["description"]
    resource_created = resource_dict["created"]
    mimetype = resource_dict["mimetype"]
    is_tiff = False
    bbox = bounding_box(package_spatial['coordinates'][0])
    footprint = package_spatial
    # if mimetype == 'image/tiff' and resource_url_type == 'upload':
    #     is_tiff = True
    #     first_folder = resource_id[0:3]
    #     second_folder = resource_id[3:6]
    #     file_name = resource_id[6:len(resource_id)]
    #     img_path = f"/home/appuser/data/resources/{first_folder}/{second_folder}/{file_name}"
    #     bbox, footprint = get_bbox_and_footprint(img_path)
    # else:
    #     bbox = bounding_box(package_spatial['coordinates'][0])
    #     footprint = package_spatial

    collection_item = pystac.Item(id=f"{resource_name}_{resource_id}",
                            geometry=footprint,
                            bbox=bbox,
                            datetime=pd.to_datetime(resource_created, infer_datetime_format=True),
                            properties={},)
    
    if is_tiff:
        collection_item.add_asset(
            key='image',
            asset=pystac.Asset(
                href=resource_url,
                media_type=pystac.MediaType.GEOTIFF
            )
        )
    collection_item.add_links([
        pystac.Link.root(f"http://localhost:5000/stac/{package_name}/item/{resource_id}"),
        pystac.Link.canonical(f"http://localhost:5000/dataset/{package_name}/resource/{resource_id}")
    ])

    # logger.debug(f"collection_item {collection_item.to_dict()}")

    return jsonify(resource_dict)

@stac_api_blueprint.route("/resourcecollection", methods = ['POST', 'GET'])
def resourcecollection():
    package_list = p.toolkit.get_action("package_list")({},{})

    items = []
    
    for package in package_list:
        package_dict = p.toolkit.get_action("package_show")({"model": model},{'id': package})
        logger.debug(f"package {package_dict}")
        package_spatial = json.loads(package_dict['spatial'])
        package_name = package_dict["name"]
        package_title = package_dict["title"]
        package_description = package_dict["notes"]
        resources = package_dict["resources"]
        package_date = package_dict["reference_date"]
        spatial_extent = pystac.SpatialExtent(bboxes=[bounding_box(package_spatial['coordinates'][0])])

        date_format = '%m/%d/%Y %H:%M:%S.%f'
        collection_interval = [pd.to_datetime(package_date, infer_datetime_format=True), datetime.now()]
        temporal_extent = pystac.TemporalExtent(intervals=[collection_interval])

        collection_extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)
        
        
        for resource in resources:
            resource_id = resource["id"]
            resource_name = resource["name"]
            resource_url = resource["url"]
            resource_url_type = resource["url_type"]
            resource_format = resource["format"]
            # resource_description = resource["description"]
            resource_created = resource["created"]
            mimetype = resource["mimetype"]
            is_tiff = False
            if mimetype == 'image/tiff' and resource_url_type == 'upload':
                is_tiff = True
                first_folder = resource_id[0:3]
                second_folder = resource_id[3:6]
                file_name = resource_id[6:len(resource_id)]
                img_path = f"/home/appuser/data/resources/{first_folder}/{second_folder}/{file_name}"
                bbox, footprint = get_bbox_and_footprint(img_path)
            else:
                bbox = bounding_box(package_spatial['coordinates'][0])
                footprint = package_spatial

            collection_item = pystac.Item(id=f"{resource_name}_{resource_id}",
                                geometry=footprint,
                                bbox=bbox,
                                datetime=pd.to_datetime(resource_created, infer_datetime_format=True),
                                properties={
                                    "description": package_description,
                                },)
            
            if is_tiff:
                collection_item.add_asset(
                    key='image',
                    asset=pystac.Asset(
                        href=resource_url,
                        media_type=pystac.MediaType.GEOTIFF
                    )
                )
            
            collection_item.add_links([
                pystac.Link.root(f"http://localhost:5000/stac/{package_name}/item/{resource_id}"),
                pystac.Link.canonical(f"http://localhost:5000/dataset/{package_name}/resource/{resource_id}")
            ])
            items.append(collection_item)
        
        collection = pystac.ItemCollection(items)
    
    return jsonify(collection.to_dict()) 

@stac_api_blueprint.route("/datasetcollection", methods = ['POST', 'GET'])
def datasetcollection():
    package_list = p.toolkit.get_action("package_list")({},{})

    items = []
    
    for package in package_list:
        package_dict = p.toolkit.get_action("package_show")({"model": model},{'id': package})
        logger.debug(f"package {package_dict}")
        package_spatial = json.loads(package_dict['spatial'])
        package_name = package_dict["name"]
        package_title = package_dict["title"]
        package_description = package_dict["notes"]
        resources = package_dict["resources"]
        package_date = package_dict["reference_date"]
        
        logger.debug(f"package details {package_dict}")

        keywords = []
        for tag in package_dict["tags"]:
            keywords.append(tag["name"])

        try:
            thumbnail = package_dict["metadata_thumbnail"]
        except KeyError:
            if package_dict["organization"]["image_url"] != "" :
                thumbnail = f'/uploads/group/{package_dict["organization"]["image_url"]}'
            else:
                thumbnail = "/images/org.png"

        if package_date is None:
            package_date = datetime.now()

        spatial_extent = pystac.SpatialExtent(bboxes=[bounding_box(package_spatial['coordinates'][0])])

        date_format = '%m/%d/%Y %H:%M:%S.%f'
        collection_interval = [pd.to_datetime(package_date, infer_datetime_format=True), datetime.now()]
        temporal_extent = pystac.TemporalExtent(intervals=[collection_interval])

        collection_extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)
        
        collection_item = pystac.Item(id=f"{package_title}",
                                geometry=package_spatial,
                                bbox=bounding_box(package_spatial['coordinates'][0]),
                                datetime=pd.to_datetime(package_date, infer_datetime_format=True),
                                properties={
                                    "name": package_title,
                                    "description": package_description,
                                    "keywords": keywords
                                },)

        collection_item.add_links([
                pystac.Link.root(f"http://localhost:5000/stac/collection/{package_name}"),
                pystac.Link.canonical(f"http://localhost:5000/dataset/{package_name}")
            ])
        
        collection_item.add_asset(
                    key='thumbnail',
                    asset=pystac.Asset(
                        href=thumbnail
                    )
                )
    
        for resource in resources:
            resource_id = resource["id"]
            resource_name = resource["name"]
            resource_url = resource["url"]
            resource_url_type = resource["url_type"]
            resource_format = resource["format"]
            # resource_description = resource["notes"]
            resource_created = resource["created"]
            mimetype = resource["mimetype"]
            collection_item.add_asset(
                    key='resource',
                    asset=pystac.Asset(
                        title = resource_name,
                        href=resource_url,
                        media_type=resource_format
                    )
                )
            
        items.append(collection_item)
        
    collection = pystac.ItemCollection(items)
    
    return jsonify(collection.to_dict()) 