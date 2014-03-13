from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos.polygon import Polygon
from owsparser import parse_wms

def service_url_validator(url):
    a = 1
    
preferred_formats = ['image/png', 'image/jpeg', 'image/geotiff', 'image/tiff']

class Layer(geomodels.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=512)
    abstract = models.TextField(null=True)
    bbox = geomodels.PolygonField(null=True)
    max_scale = models.FloatField(null=True)
    min_scale = models.FloatField(null=True)
    service = models.ForeignKey('Service')
    
    objects = geomodels.GeoManager()

class Service(geomodels.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=512,validators=[service_url_validator])
    bbox = geomodels.PolygonField(null=True,blank=True)
    getmapurl = models.CharField(max_length=512,blank=True)
    getmapformats = models.CharField(max_length=255,blank=True)
    abstract = models.TextField(null=True,blank=True)
    keywords = models.CharField(max_length=512,null=True,blank=True)
    
    objects = geomodels.GeoManager()
    
    def get_wms(self,url):
        return parse_wms(url)
    
    def make_polybbox(self,bbox):
        return Polygon.from_bbox(bbox)
    
    def extend_bbox(self,layer_bbox,overall_bbox):
        if overall_bbox:
            _xmin,_ymin,_xmax,_ymax = layer_bbox
            xmin,ymin,xmax,ymax = overall_bbox
            xmin = min(_xmin,xmin)
            ymin = min(_ymin,ymin)
            xmax = max(_xmax,xmax)
            ymax = max(_ymax,ymax)
            return xmin,ymin,xmax,ymax
        else:
            return layer_bbox

    def get_preferred_format(self):
        formats = self.getmapformats.split(' ')
        for f in preferred_formats:
            if f in formats:
                return f
    
    def save(self,force_insert=False, force_update=False, using=None,update_fields=None):
        if not self.pk:
            wms = self.get_wms(self.url)
            self.set_service_metadata(wms)
            overall_bbox = None
            layers = []
            for layer in wms.contents:
                layer_obj = Layer()
                layer_obj.title = wms[layer].title
                layer_obj.name = wms[layer].name
                layer_obj.abstract = wms[layer].abstract
                if wms[layer].scaleHint:
                    layer_obj.min_scale = wms[layer].scaleHint.get('min',None)
                    layer_obj.max_scale = wms[layer].scaleHint.get('max',None)
                layer_bbox = wms[layer].boundingBoxWGS84
                print layer_bbox
                overall_bbox = self.extend_bbox(layer_bbox, overall_bbox)
                layer_obj.bbox = self.make_polybbox(layer_bbox)
                layers.append(layer_obj)
            self.bbox = self.make_polybbox(overall_bbox)
            super(Service,self).save(force_insert,force_update,using,update_fields)
            self.layer_set = layers
        else:
            super(Service,self).save(force_insert,force_update,using,update_fields)
        
    def set_service_metadata(self,wms):
        self.abstract = wms.identification.abstract
        self.keywords = ' '.join(wms.identification.keywords)
        if wms.getOperationByName('GetMap').methods.get('Get',None):
            self.getmapurl = wms.getOperationByName('GetMap').methods['Get']['url']
        self.getmapformats = ' '.join(wms.getOperationByName('GetMap').formatOptions)
