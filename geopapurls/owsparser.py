from owslib.wms import WebMapService

def parse_wms(url):
    wms = WebMapService(url, version='1.1.1')
    return wms
