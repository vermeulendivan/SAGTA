from qgis.server import *
from qgis.core import QgsMessageLog, Qgis, QgsExpression, QgsProject, QgsCoordinateTransform, \
    QgsCoordinateReferenceSystem
from qgis.utils import qgsfunction, iface
from qgis.gui import *


def map_bounds(composer_title, map_id):
    project_instance = QgsProject.instance()
    project_layout_manager = project_instance.layoutManager()
    layout = project_layout_manager.layoutByName(composer_title)
    map = layout.itemById(map_id)
    transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:3857"),
                                       QgsCoordinateReferenceSystem("EPSG:4326"), project_instance)
    bbox = map.extent()
    extent = transform.transformBoundingBox(bbox)
    return extent


@qgsfunction(args='auto', group='Custom')
def map_x_min(composer_title, map_id, feature, parent):
    map_extent = map_bounds(composer_title, map_id)
    x_min = map_extent.xMinimum()
    return x_min


@qgsfunction(args='auto', group='Custom')
def map_x_max(composer_title, map_id, feature, parent):
    map_extent = map_bounds(composer_title, map_id)
    x_max = map_extent.xMaximum()
    return x_max


@qgsfunction(args='auto', group='Custom')
def map_y_min(composer_title, map_id, feature, parent):
    map_extent = map_bounds(composer_title, map_id)
    y_min = map_extent.yMinimum()
    return y_min


@qgsfunction(args='auto', group='Custom')
def map_y_max(composer_title, map_id, feature, parent):
    map_extent = map_bounds(composer_title, map_id)
    y_max = map_extent.yMaximum()
    return y_max


class MapExpressionPlugin:
    def __init__(self):
        QgsMessageLog.logMessage('Loading expressions', 'MapExpression', Qgis.Info)
        QgsExpression.registerFunction(map_x_min)
        QgsExpression.registerFunction(map_x_max)
        QgsExpression.registerFunction(map_y_min)
        QgsExpression.registerFunction(map_y_max)


def serverClassFactory(serverIface):
    _ = serverIface
    return MapExpressionPlugin()

