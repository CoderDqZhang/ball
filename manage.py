#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
<<<<<<< HEAD
reload(sys)
sys.setdefaultencoding('utf8')
=======

import importlib
importlib.reload(sys)

sys.setdefaultencoding('utf8')

>>>>>>> 7c72ceb493cd818bbe206050de3c2bb4cffa99d6
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ball.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
