from owslib.wms import WebMapService
from django.core.management.base import BaseCommand, CommandError
from geopapurls.models import Service

class Command(BaseCommand):
    help = 'Fetch title from WMS services in DB'

    def handle(self, *args, **options):
        services = Service.objects.all()
        for service in services:
            try:
                wms = WebMapService(service.url,version='1.1.1')
                self.stdout.write('Service ID %s: %s' % (service.id,wms.identification.title))
            except Exception,e:
                raise CommandError('Error on service %s: %s' % (service.id,str(e)))