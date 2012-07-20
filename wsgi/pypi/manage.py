#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))

    try:
        # activate virtualenv
        virtenv = os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 'virtenv')
        activate_this = os.path.join(virtenv, 'bin', 'activate_this.py')
        execfile(activate_this, dict(__file__=activate_this))
    except:
        pass

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
