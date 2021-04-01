import json
from datetime import datetime
from os import environ
from urllib import parse, request
from urllib.error import HTTPError

from qgis.core import QgsMessageLog, Qgis, QgsExpression, QgsGeometry, QgsRectangle
from qgis.utils import qgsfunction


def map_bounds():
    layout_extent = environ.get('TRANSFORMED_EXTENT')
    extent = [float(i) for i in layout_extent.split(',')]
    geometry_extent = QgsGeometry.fromRect(QgsRectangle(extent[0], extent[1], extent[2], extent[3]))
    coordinates = geometry_extent.centroid()

    return coordinates


def json_response(url):
    try:
        data = request.urlopen(url)
        error_code = data.getcode()
    except HTTPError as error:
        error_code = error.code
    if error_code == 200:
        response = data.read()
        response_text = response.decode('utf-8')
    else:
        response_text = None
    return response_text


@qgsfunction(args='auto', group='Custom')
def map_decl(feature, parent):
    lat = map_bounds().get().x()
    long = map_bounds().get().y()
    # Calculate elevation from Geocontext
    elevation_url = "https://geocontext.kartoza.com/api/v1/geocontext/value/group/%s/%s/elevation_group/?format=json" \
                    % (lat, long)
    elevation_response_text = json_response(elevation_url)
    if elevation_response_text is not None:
        elevation_response_json = json.loads(elevation_response_text)["service_registry_values"][0]
        elevation_value = elevation_response_json['value']
    else:
        elevation_value = 'Site is not up'
    now = datetime.now()
    month = now.month
    month_name = now.strftime('%B')
    month_day = now.day
    current_year = now.year
    params = parse.urlencode({'lat1': lat, 'lon1': long, 'resultFormat': 'json', 'startMonth': month})
    mag_url = "http://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination?%s" % params
    mag_response_text = json_response(mag_url)
    if mag_response_text is not None:
        mag_response_json = json.loads(mag_response_text)["result"][0]
        magnetic_declination = mag_response_json["declination"]
        if lat > 0:
            lat_label = 'N'
        else:
            lat_label = 'S'
        if long > 0:
            long_label = 'E'
        else:
            long_label = 'W'

        formatted_label = '%s %s\n%s %s\n%s%s\n%s %s %s\n%s%s%s' % (
            lat_label, round(lat, 4), long_label, round(long, 4), 'Mag Declination ', magnetic_declination, month_day,
            month_name, current_year, 'Elevation: ', elevation_value, 'm')
    else:
        formatted_label = None
        magnetic_declination = None

    return [formatted_label, magnetic_declination]


class MagneticDeclinationPlugin:
    def __init__(self):
        QgsMessageLog.logMessage('Loading expressions', 'MagneticDeclination', Qgis.Info)
        QgsExpression.registerFunction(map_decl)


def serverClassFactory(serverIface):
    _ = serverIface
    return MagneticDeclinationPlugin()

