"""
ASGI config for energy_monitoring project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energy_monitoring.settings")

application = get_asgi_application()
