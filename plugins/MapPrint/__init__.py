# -*- coding: utf-8 -*-

def serverClassFactory(serverIface):
    from .MapPrint import MapPrint
    return MapPrint(serverIface)

