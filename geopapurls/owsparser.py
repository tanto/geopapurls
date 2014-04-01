from owslib.wms import WebMapService

zooms = range(0,23)
RADIUS_GOOGLE_EARTH = 6378137
res = lambda x:RADIUS_GOOGLE_EARTH*3.14*2/(256*(2**x))
RESOLUTIONS = [res(z) for z in zooms]

def parse_wms(url):
    wms = WebMapService(url, version='1.1.1')
    return wms
