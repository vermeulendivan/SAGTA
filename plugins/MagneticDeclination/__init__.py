import json
from datetime import datetime
from os import environ
from urllib import parse, request

from qgis.core import QgsMessageLog, Qgis, QgsExpression, QgsGeometry, QgsRectangle
from qgis.utils import qgsfunction


def map_bounds():
    layout_extent = environ.get('TRANSFORMED_EXTENT')
    print(layout_extent)
    QgsMessageLog.logMessage("Transformed extent", environ['TRANSFORMED_EXTENT'], Qgis.Info)
    extent = [float(i) for i in layout_extent.split(',')]
    geometry_extent = QgsGeometry.fromRect(QgsRectangle(extent[0], extent[1], extent[2], extent[3]))
    coordinates = geometry_extent.centroid()

    return coordinates


def json_response(url):
    data = request.urlopen(url)
    response = data.read()
    response_text = response.decode('utf-8')
    return response_text


@qgsfunction(args='auto', group='Custom')
def map_decl(feature, parent):
    lat = map_bounds().get().x()
    long = map_bounds().get().y()
    # Calculate elevation from Geocontext
    elevation_url = "https://geocontext.kartoza.com/api/v1/geocontext/value/group/%s/%s/elevation_group/?format=json" \
                    % (lat, long)
    elevation_response_text = json_response(elevation_url)
    elevation_response_json = json.loads(elevation_response_text)["service_registry_values"][0]
    elevation_value = elevation_response_json['value']
    now = datetime.now()
    month = now.month
    month_name = now.strftime('%B')
    month_day = now.day
    current_year = now.year
    params = parse.urlencode({'lat1': lat, 'lon1': long, 'resultFormat': 'json', 'startMonth': month})
    mag_url = "http://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination?%s" % params
    mag_response_text = json_response(mag_url)

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

    formatted_label = '%s %s\n%s %s\n%s%s \n%s %s %s\n%s %s%s' % (
        lat_label, round(lat, 4), long_label, round(long, 4), 'Mag Decl: ', magnetic_declination, month_day, month_name,
        current_year, 'Elevation: ', int(elevation_value), 'm')

    return [formatted_label, magnetic_declination]


class MapExpressionPlugin:
    def __init__(self):
        QgsMessageLog.logMessage('Loading expressions', 'MagneticDeclination', Qgis.Info)
        QgsExpression.registerFunction(map_decl)


def serverClassFactory(serverIface):
    _ = serverIface
    return MapExpressionPlugin()
