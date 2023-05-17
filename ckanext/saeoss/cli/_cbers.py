import xml.dom.minidom as dom
from ._parse_date_time import parse_date_time
from ..constants import PROJECTION


def get_geometry(log_message, dom):
    """Extract the bounding box as a geometry from the xml file.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: DOM Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: geoemtry
    """
    up_left_lat_value = dom.getElementsByTagName('productUpperLeftLat')[0]
    up_left_lat = up_left_lat_value.firstChild.nodeValue

    up_left_long_value = dom.getElementsByTagName('productUpperLeftLong')[0]
    up_left_long = up_left_long_value.firstChild.nodeValue

    up_right_lat_value = dom.getElementsByTagName('productUpperRightLat')[0]
    up_right_lat = up_right_lat_value.firstChild.nodeValue

    up_right_long_value = dom.getElementsByTagName('productUpperRightLong')[0]
    up_right_long = up_right_long_value.firstChild.nodeValue

    low_left_lat_value = dom.getElementsByTagName('productLowerLeftLat')[0]
    low_left_lat = low_left_lat_value.firstChild.nodeValue

    low_left_long_value = dom.getElementsByTagName('productLowerLeftLong')[0]
    low_left_long = low_left_long_value.firstChild.nodeValue

    low_right_lat_value = dom.getElementsByTagName('productLowerRightLat')[0]
    low_right_lat = low_right_lat_value.firstChild.nodeValue

    low_right_long_value = dom.getElementsByTagName('productLowerRightLong')[0]
    low_right_long = low_right_long_value.firstChild.nodeValue


    polygon = 'POLYGON((' '%s %s, ' \
              '%s %s, %s %s, %s %s, %s %s' '))' % (
                  up_left_long, up_left_lat,
                  up_right_long, up_right_lat,
                  low_right_long, low_right_lat,
                  low_left_long, low_left_lat,
                  up_left_long, up_left_lat)

    log_message('Geometry: %s' % polygon, 2)
    return polygon


def get_dates(log_message, dom):
    """Get the start, mid scene and end dates.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: A two-tuple of dates for the start, and mid scene
        respectively.
    :rtype: (datetime, datetime)
    """
    start_element = dom.getElementsByTagName('imagingStartTime')[0]
    start_date = start_element.firstChild.nodeValue
    start_date = parse_date_time(start_date)
    log_message('Product Start Date: %s' % start_date, 2)

    product_date = dom.getElementsByTagName('productDate')[0]
    center_date = product_date.firstChild.nodeValue
    center_date = parse_date_time(center_date)
    log_message('Product Date: %s' % center_date, 2)

    return start_date, center_date


def get_original_product_id(filename):
    # Get part of product name from filename
    # file name = CB04-WFI-81-135-20160118-L20000024812
    tokens = filename.split('-')
    product_name = ''.join(tokens)
    return product_name


def get_band_count(dom):
    band_count_data = dom.getElementsByTagName('bands')[0]
    band_count = band_count_data.firstChild.nodeValue
    if len(band_count) == 1:
        return 1
    else:
        return len(eval(band_count))


def get_solar_azimuth_angle(dom):
    sun_azimuth = dom.getElementsByTagName('sunAzimuthElevation')[0]
    solar_azimuth = sun_azimuth.firstChild.nodeValue
    return solar_azimuth


def get_scene_row(dom):
    scene_row = dom.getElementsByTagName('sceneRow')[0]
    row = scene_row.firstChild.nodeValue
    return row


def get_scene_path(dom):
    scene_path = dom.getElementsByTagName('scenePath')[0]
    path = scene_path.firstChild.nodeValue
    return path


def get_sensor_inclination():
    # The static value of sensor inclination angle
    # source http://www.cbers.inpe.br/ingles/satellites/orbit_cbers3_4.php
    return 98.5


def get_spatial_resolution_x(dom):
    spatial_resolution_data = dom.getElementsByTagName('pixelSpacing')[0]
    spatial_resolution = spatial_resolution_data.firstChild.nodeValue
    return spatial_resolution


def get_spatial_resolution_y(dom):
    spatial_resolution_data = dom.getElementsByTagName('pixelSpacing')[0]
    spatial_resolution = spatial_resolution_data.firstChild.nodeValue
    return spatial_resolution


def get_projection(dom):
    """Get the projection for this product record.

    The project is always expressed as an EPSG code and we fetch the related
    Projection model for that code.

    :param specific_parameters: Dom Document containing the bounds of the scene.
    :type specific_parameters: DOM document.

    :returns: A projection model for the specified EPSG.
    :rtype: Projection
    """
    epsg_default_code = '32'
    get_zone = dom.getElementsByTagName('zone')[0]
    zone_value = get_zone.firstChild.nodeValue
    zone = zone_value[0:2]
    location_code = '7'  # 6 for north and 7 for south
    epsg_code = epsg_default_code + location_code + zone

    projection = 'EPSG: %s %s' % (epsg_code, PROJECTION[epsg_code])
    return projection


def get_radiometric_resolution(dom):
    """Get the radiometric resolution for the supplied product record.
    source = http://www.cbers.inpe.br/ingles/satellites/cameras_cbers3_4.php

    MUXCAM = 8 bits
    PANMUX = 8 bits
    IRSCAM = 8 bits
    WFICAM = 10 bits

    :param resolution_element: Dom Document containing the bounds of the scene.
    :type resolution_element: DOM document.

    :returns: The bit depth for the image.
    :rtype: int
    """
    get_sensor_id = dom.getElementsByTagName('sensorId')[0]
    sensor_id = get_sensor_id.firstChild.nodeValue
    # sensor_id : MUX, P10, P5M, WFI
    if sensor_id == 'MUX':
        return 8
    elif sensor_id == 'P10':
        return 8
    elif sensor_id == 'P5M':
        return 8
    elif sensor_id == 'WFI':
        return 10
    else:
        return 0


def get_quality(dom):
    """Get the quality for this record - currently hard coded to unknown.

    :returns: A quality object fixed to 'unknown'.
    :rtype: Quality
    """
    overall_quality = dom.getElementsByTagName('overallQuality')[0]
    return str(overall_quality.firstChild.nodeValue)
