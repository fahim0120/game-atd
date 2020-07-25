"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys



path = "/home/gameatd/mysite"

if path not in sys.path:
    sys.path.append(path)

print (sys.path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
