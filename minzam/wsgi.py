"""
WSGI config for minzam project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from main_app.task_notifier import run_task_notifier

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minzam.settings')

application = get_wsgi_application()

run_task_notifier()
