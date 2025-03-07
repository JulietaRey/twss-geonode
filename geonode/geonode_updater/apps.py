from django.apps import AppConfig

class GeoNodeUpdaterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geonode.geonode_updater"

    def ready(self):
        """Se ejecuta al iniciar Django"""
        from geonode.geonode_updater.views import schedule_update
        schedule_update()  # ✅ Programa la tarea automáticamente al iniciar
