#!/usr/bin/env python
import os
import sys
import glob

if __name__ == "__main__":
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
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

