from django.utils.timezone import now
from django_q.models import Schedule

def schedule_update():
    """ Programa la actualización del GeoJSON en GeoNode cada 2 minutos """
    Schedule.objects.update_or_create(
        func="geonode.geonode_updater.tasks.upload_to_geonode",
        defaults={
            "schedule_type": Schedule.MINUTES,  # ✅ Ejecutar cada X minutos
            "minutes": 5,  # ✅ Intervalo de 5 minutos
            "next_run": now()
        },
    )
