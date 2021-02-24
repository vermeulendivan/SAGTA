import re
from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.server import *
import os


class MapPrint:
   

    def __init__(self, serverIface):
        self.serverIface = serverIface
        serverIface.registerFilter(MapPrintFilter(serverIface), 100)

class MapPrintFilter(QgsServerFilter):

    def __init__(self, serverIface):
        super(MapPrintFilter, self).__init__(serverIface)

    def requestReady(self):
        request = self.serverInterface().requestHandler()

        params = request.parameterMap()
        if params.get('REQUEST') != None and params.get('REQUEST').upper() == 'GETPRINT':
            QgsMessageLog.logMessage("INSIDE Print Filter, setting map extent", 'Map Print Filter', Qgis.Info)
            os.environ['MAP_EXTENT'] = params.get('MAP0:EXTENT')