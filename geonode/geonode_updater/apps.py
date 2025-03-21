from django.apps import AppConfig
from django.db.models.signals import post_migrate

class GeoNodeUpdaterConfig(AppConfig):
    name = 'geonode.geonode_updater'
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from .signals import schedule_task_post_migrate
        post_migrate.connect(schedule_task_post_migrate, sender=self)