from qgis.server import *
from qgis.core import QgsMessageLog, Qgis, QgsExpression, QgsProject
from qgis.utils import qgsfunction
import os


@qgsfunction(
    args='auto', group='custom', usesGeometry=False, referencedColumns=[], helpText='Define the help string here')

def map_index(source_layer, map_extent, source_attribute, feature, parent):
    project = QgsProject.instance()

    QgsMessageLog.logMessage('Extent', 'LabelExpression', Qgis.Info)
    QgsMessageLog.logMessage(os.environ.get('MAP_EXTENT'), 'LabelExpression', Qgis.Info)

    project.read('../srv/projects/map_downloader/topomaps.qgs')
    map_layer = project.mapLayersByName(source_layer)[0]
    map_extent_bounds = map_extent.boundingBox()

    QgsMessageLog.logMessage(map_extent_bounds, 'LabelExpression', Qgis.Info)
    records = []
    for f in map_layer.getFeatures():
        f_bounds = f.geometry().boundingBox()
        if map_extent_bounds.intersects(f_bounds):
            field_name_idx = f.fieldNameIndex(source_attribute)
            field_value = f.attributes()[field_name_idx]
            records.append(field_value)
    result = '\n'.join(records)
    QgsMessageLog.logMessage('Results', 'LabelExpression', Qgis.Info)
    QgsMessageLog.logMessage(result, 'LabelExpression', Qgis.Info)
    return result


class LabelExpressionPlugin:
    def __init__(self):
        QgsMessageLog.logMessage('Loading expressions', 'LabelExpression', Qgis.Info)
        QgsExpression.registerFunction(map_index)

def serverClassFactory(serverIface):
    _ = serverIface
    return LabelExpressionPlugin()
