import json
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import HttpResponse
from models import Layer
       
mapurl_template = '''url={url}
minzoom=11
maxzoom=22
center= {x_center} {y_center}
type=wms
format={format}
defaultzoom=17
bounds={bbox}
description={description}
mbtiles=wmslayers/{uid}.mbtiles
'''

url_template = '{baseurl}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS={layername}&SRS=EPSG:4326&FORMAT={imageformat}&BBOX=XXX,YYY,XXX,YYY&WIDTH=256&HEIGHT=256'
        
class CommonListView(ListView):
    model = Layer
    
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
        mapformat = layer.service.get_preferred_format()
        url = "%s?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=%s&SRS=EPSG:4326&FORMAT=%s&BBOX=XXX,YYY,XXX,YYY&WIDTH=256&HEIGHT=256" % (service_url,layer.name,mapformat)
        return url

class LayersView(CommonListView):
    pass

    def get_context_data(self, **kwargs):
        context = super(LayersView, self).get_context_data(**kwargs)
        #context['getmapurl'] = 
        return context

class MapurlsView(CommonListView):
   
    def get(self,request):
        layers = self.filter_queryset(request).all()
        print len(layers)
        layers_list = []
        for layer in layers:
            layer_dict = {}
            layer_dict['title'] = layer.title
            layer_dict['id'] = layer.id
            layers_list.append(layer_dict)

        layers_json = json.dumps(layers_list)
        return HttpResponse(layers_json, mimetype='application/json')
    

class MapurlDetailView(DetailView):
    model = Layer
    admitted_actions = ['download']
    
    def get(self, request, *args, **kwargs):
        action = kwargs.get('action',None)
        if action and action in self.admitted_actions:
            action_method = getattr(self,'action_'+action)
        else:
            action_method = self.action_default
        return action_method()
    
    def action_download(self):
        mapurl_file = StringIO()
        self.object = self.get_object()
        response_text = self.make_from_template()
        mapurl_file.write(response_text)
        response = HttpResponse(FileWrapper(mapurl_file), content_type='application/mapurl')
        response['Content-Disposition'] = 'attachment; filename='+str(self.object.pk)+'.mapurl'
        response['Content-Length'] = mapurl_file.tell()
        mapurl_file.seek(0)
        return response
    
    def action_default(self):
        self.object = self.get_object()
        response_text = self.make_from_template()
        response = HttpResponse(mimetype='text/plain')
        response.write('%s\n' % response_text)
        return response
    
    def make_from_template(self):
        mapurl_dict = {}
        baseurl = self.object.service.getmapurl if self.object.service.getmapurl else self.object.service.url
        mapurl_dict['url'] = url_template.format(**{'baseurl':baseurl,'layername':self.object.name,'imageformat':self.object.service.get_preferred_format()})
        mapurl_dict['x_center'] = self.object.bbox.centroid.x
        mapurl_dict['y_center'] = self.object.bbox.centroid.y
        mapurl_dict['bbox'] = ' '.join(map(str,self.object.bbox.extent))
        mapurl_dict['format'] = self.object.service.get_preferred_format().replace('image/','')
        mapurl_dict['description'] = self.object.name
        mapurl_dict['uid'] = self.object.pk
        return mapurl_template.format(**mapurl_dict)
        
    