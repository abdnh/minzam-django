from django.apps import AppConfig

from .task_notifier import run_task_notifier

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'
    verbose_name = 'منظام'

    def ready(self):
        run_task_notifier()
