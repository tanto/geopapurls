import json
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from models import Layer,Suggestion
from forms import SuggestForm
from django.views.generic.edit import CreateView
       
mapurl_template = '''url={url}
minzoom=11
maxzoom=22
center= {x_center} {y_center}
type=wms
format={format}
defaultzoom=17
bounds={bbox}
description={description}
mbtiles=wmslayers/_tanto_{uid}.mbtiles
'''

url_template = '{baseurl}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS={layername}&SRS=EPSG:4326&FORMAT={imageformat}&BBOX=XXX,YYY,XXX,YYY&WIDTH=256&HEIGHT=256'

def home(request):
    return redirect('suggest')

class CommonListView(ListView):
    model = Layer
    
    def get_queryset(self):
        queryset = super(CommonListView,self).get_queryset().order_by('-id')
        request = self.request
        specific_filter = getattr(self.__class__,'specific_filer',None)
        if specific_filter:
            queryset = queryset.filter(specific_filter)
        results_per_page = getattr(self.__class__,'max_res_per_page',None) or settings.MAX_RESULTS_PER_PAGE
        offset = 0
        query = request.GET
        p = query.get('p',None)
        if p:
            try:
                coords = p.split(',')
                x = float(coords[0])
                y = float(coords[1])
                queryset = queryset.filter(bbox__contains="POINT(%s %s)" % (x,y))
            except:
                pass
        t = query.get('t',None)
        if t:
            qtitle = Q(title__icontains=t)
            qabstract = Q(abstract__icontains=t)
            queryset = queryset.filter(qtitle | qabstract)
        query_limit = query.get('l',None)
        if query_limit:
            try:
                limit = int(query_limit)
                results_per_page = min(limit,results_per_page)
            except:
                pass
        query_offset = query.get('o',None)
        if query_offset:
            try:
                offset = int(query_offset)
            except:
                pass
        results_per_page = results_per_page + offset
        return queryset[offset:results_per_page]
    
    def make_url(self,layer):
        service_url = layer.service.getmapurl if layer.service.getmapurl else layer.service.url
        mapformat = layer.service.get_preferred_format()
        url = "%s?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=%s&SRS=EPSG:4326&FORMAT=%s&BBOX=XXX,YYY,XXX,YYY&WIDTH=256&HEIGHT=256" % (service_url,layer.name,mapformat)
        return url

class LayersView(CommonListView):
    max_res_per_page = 10000000
    paginate_by = settings.MAX_RESULTS_PER_PAGE

class MapurlsView(CommonListView):
    # For Geopaparazzi mapurls we only support WGS84 enabled services
    specific_filer = Q(supports_4326=True)
    max_res_per_page = 10000000    

    def get(self,request):
        layers = self.get_queryset().all()
        print len(layers)
        layers_list = []
        for layer in layers:
            layer_dict = {}
            layer_dict['id'] = layer.id
            layer_dict['title'] = layer.title
            layer_dict['service'] = layer.service.name
            layers_list.append(layer_dict)

        layers_json = json.dumps(layers_list)
        return HttpResponse(layers_json, mimetype='application/json')
    

class MapurlDetailView(DetailView):
    model = Layer
    admitted_actions = ['download','preview']
    
    def get(self, request, *args, **kwargs):
        action = kwargs.get('action',None)
        if action and action in self.admitted_actions:
            action_method = getattr(self,'action_'+action)
        else:
            action_method = self.action_default
        return action_method(request, *args, **kwargs)
    
    def action_download(self, request, *args, **kwargs):
        mapurl_file = StringIO()
        self.object = self.get_object()
        response_text = self.make_from_template()
        mapurl_file.write(response_text)
        response = HttpResponse(FileWrapper(mapurl_file), content_type='application/mapurl')
        response['Content-Disposition'] = 'attachment; filename=tanto_%s.mapurl' % str(self.object.pk)
        response['Content-Length'] = mapurl_file.tell()
        mapurl_file.seek(0)
        return response
    
    def action_default(self, request, *args, **kwargs):
        self.object = self.get_object()
        response_text = self.make_from_template()
        response = HttpResponse(mimetype='text/plain')
        response.write('%s\n' % response_text)
        return response
    
    def action_preview(self, request, *args, **kwargs):
        return super(MapurlDetailView,self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MapurlDetailView,self).get_context_data(**kwargs)
        context['bounds_xmin'] = self.object.bbox.extent[0]
        context['bounds_ymin'] = self.object.bbox.extent[1]
        context['bounds_xmax'] = self.object.bbox.extent[2]
        context['bounds_ymax'] = self.object.bbox.extent[3]
        return context
    
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
    
class SuggestView(CreateView):
    model = Suggestion
    form_class = SuggestForm
    template_name = 'geopapurls/suggest.html'
    
    def get_success_url(self):
        return reverse('thanks')
        
    
