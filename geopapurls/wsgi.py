"""
WSGI config for geopapurls project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import glob

os.chdir('/home/apps/geopapurls')

if 'test' in sys.argv:
    env_dir = os.path.join('tests', 'config')
else:
    env_dir = 'config'
env_vars = glob.glob(os.path.join(env_dir, '*'))
for env_var in env_vars:
    with open(env_var, 'r') as env_var_file:
        key = env_var.split(os.sep)[-1]
        val = env_var_file.read().strip()
        os.environ.setdefault(key,val)
os.environ['DJANGO_SETTINGS_MODULE'] = 'geopapurls.settings'
sys.path.append('/home/apps/geopapurls')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

