import json
from django.views.generic import ListView
from django.db.models import Q
from django.http import HttpResponse
from models import Layer

preferred_formats = ['image/png', 'image/jpeg', 'image/geotiff', 'image/tiff']

def get_preferred_format(formats):
    formats = formats.split(' ')
    for f in preferred_formats:
        if f in formats:
            return f

class LayersView(ListView):
    model = Layer
    
    def get(self,request):
        layers = self.filter_queryset(request).all()
        print len(layers)
        layers_list = []
        for layer in layers:
            layer_dict = {}
            layer_dict['title'] = layer.title
            layer_dict['url'] = self.make_url(layer)
            layer_dict['bbox'] = ' '.join(map(str,layer.bbox.extent))
            layer_dict['format'] = get_preferred_format(layer.service.getmapformats).replace('image/','')
            layer_dict['center'] = "%s %s" % (layer.bbox.centroid.x,layer.bbox.centroid.y)
            #layer_dict['type'] = 'WMS'
            #layer_dict['min_scale'] = layer.min_scale
            #layer_dict['max_scale'] = layer.max_scale
            #layer_dict['abstract'] = layer.abstract
            layers_list.append(layer_dict)

        layers_json = json.dumps(layers_list)
        return HttpResponse(layers_json, mimetype='application/json')
    
    def filter_queryset(self,request):
        queryset = self.get_queryset()
        query = request.GET
        ll = query.get('ll',None)
        if ll:
            coords = ll.split(',')
            x = coords[0]
            y = coords[1]
            queryset = queryset.filter(bbox__contains="POINT(%s %s)" % (x,y))
        s = query.get('s',None)
        if s:
            qtitle = Q(title__icontains=s)
            qabstract = Q(abstract__icontains=s)
            queryset = queryset.filter(qtitle | qabstract)
        return queryset
    
    def make_url(self,layer):
        service_url = layer.service.getmapurl if layer.service.getmapurl else layer.service.url
        mapformat = get_preferred_format(layer.service.getmapformats)
        url = "%s?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=%s&SRS=EPSG:4326&FORMAT=%s&BBOX=XXX,YYY,XXX,YYY&WIDTH=256&HEIGHT=256" % (service_url,layer.name,mapformat)
        return url