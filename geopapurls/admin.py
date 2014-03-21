from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from .models import *

class LayerAdminInline(admin.TabularInline):
    model = Layer
    exclude = ('bbox',)
    
    def has_add_permission(self, request):
        return False
    
    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.module_name),  args=[instance.id] )
        return mark_safe(u'<a href="{u}">Edit</a>'.format(u=url))

    readonly_fields = ('admin_link',)


class ServiceAdmin(OSMGeoAdmin):
    model = Service
    modifiable = False
    
    def admintitle(self,obj):
        return ("%s" % obj.name)
    admintitle.short_description = 'Layer WMS'
    
    list_display = ('admintitle',)
    readonly_fields = ('getmapurl','getmapformats','abstract','keywords')
    
    inlines = [
        LayerAdminInline,
    ]
    
class LayerAdmin(OSMGeoAdmin):
    model = Layer
    exclude = ('service',)
    modifiable = False
    
    def has_add_permission(self, request):
        return False
    
    def admintitle(self,obj):
        return ("%s" % obj.name)
    admintitle.short_description = 'Servizi WMS'
    
    list_display = ('admintitle',)
    
class SuggestionAdmin(admin.ModelAdmin):
    model = Suggestion
    
    def admintitle(self,obj):
        return ("%s" % obj.url)
    admintitle.short_description = 'Servizi suggeriti'
    
    list_display = ('admintitle',)
    
admin.site.register(Service,ServiceAdmin)
admin.site.register(Layer,LayerAdmin)
admin.site.register(Suggestion,SuggestionAdmin)
