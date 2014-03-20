from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos.polygon import Polygon
from owsparser import parse_wms
    
preferred_formats = ['image/png', 'image/jpeg', 'image/geotiff', 'image/tiff']
crs_4326 = 'EPSG:4326'
crs_3857 = 'EPSG:3857'

class WMSField(models.CharField):
    def validate(self,value,obj):
        try:
            obj.wms = parse_wms(value)
        except:
            raise ValidationError("The supplied URL is not valid",code="invalid")

# for South custom field management
try: 
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^geopapurls\.models\.WMSField"])
except:
    pass

class Layer(geomodels.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=512)
    abstract = models.TextField(null=True)
    bbox = geomodels.PolygonField(null=True)
    max_scale = models.FloatField(null=True)
    min_scale = models.FloatField(null=True)
    crs = models.TextField(blank=True)
    supports_4326 = models.BooleanField(default=False)
    supports_3857 = models.BooleanField(default=False)
    service = models.ForeignKey('Service')
    
    objects = geomodels.GeoManager()
    
    def supported_crs(self):
        supported_crs = []
        if self.supports_4326:
            supported_crs.append('WGS84')
        if self.supports_3857:
            supported_crs.append('Google Mercator')
        return ' - '.join(supported_crs)


class Service(geomodels.Model):
    name = models.CharField(max_length=255)
    url = WMSField(max_length=512)
    bbox = geomodels.PolygonField(null=True,blank=True)
    getmapurl = models.CharField(max_length=512,blank=True)
    getmapformats = models.CharField(max_length=255,blank=True)
    abstract = models.TextField(null=True,blank=True)
    keywords = models.CharField(max_length=512,null=True,blank=True)
    
    objects = geomodels.GeoManager()
    
    def __init__(self, *args, **kwargs):
        super(Service,self).__init__(*args, **kwargs)
        self.wms = None
        self.layers_to_save = []
    
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
            
    def clean(self, *args, **kwargs):
        self.prepare_layers_to_save()
        if not len(self.layers_to_save):
            raise ValidationError('No layer supports WGS84 ot Google Mercator projection') 
        super(Service,self).clean(*args, **kwargs)
        
    def prepare_layers_to_save(self):
        for layer in self.wms.contents:
            crsoptions = self.wms[layer].crsOptions
            supports_4326 = crs_4326 in crsoptions
            supports_3857 = crs_3857 in crsoptions
            # we only support services with WGS84 and/or Google Mercator enabled
            if supports_4326 or supports_3857:
                self.layers_to_save.append(self.wms[layer])
    
    def save(self,force_insert=False, force_update=False, using=None,update_fields=None):
        if not self.pk:
            self.set_service_metadata(self.wms)
            overall_bbox = None
            layers = []
            for layer in self.layers_to_save:
                layer_obj = Layer()
                crsoptions = layer.crsOptions
                layer_obj.crs = ' '.join(crsoptions)
                supports_4326 = crs_4326 in crsoptions
                supports_3857 = crs_3857 in crsoptions
                layer_obj.supports_4326 = supports_4326
                layer_obj.supports_3857 = supports_3857
                layer_obj.title = layer.title
                layer_obj.name = layer.name
                layer_obj.abstract = layer.abstract
                if layer.scaleHint:
                    layer_obj.min_scale = layer.scaleHint.get('min',None)
                    layer_obj.max_scale = layer.scaleHint.get('max',None)
                layer_bbox = layer.boundingBoxWGS84
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
