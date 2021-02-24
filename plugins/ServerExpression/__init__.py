from qgis.server import *
from qgis.core import QgsMessageLog, Qgis, QgsExpression
from qgis.utils import qgsfunction

@qgsfunction(
    args='auto', group='Your group', usesGeometry=False, referencedColumns=[], helpText='Define the help string here')
def your_expression(params, feature, parent):
    # UPDATE the qgsfunction above
    # ADD HERE THE EXPRESSION CODE THAT YOU WROTE IN QGIS.
    return params.upper()

class ServerExpressionPlugin:
    def __init__(self):
        QgsMessageLog.logMessage('Loading expressions', 'ServerExpression', Qgis.Info)
        QgsExpression.registerFunction(your_expression)

def serverClassFactory(serverIface):
    _ = serverIface
    return ServerExpressionPlugin()
