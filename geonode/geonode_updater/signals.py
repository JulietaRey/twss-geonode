from django_q.models import Schedule

def schedule_task_post_migrate(sender, **kwargs):
    Schedule.objects.update_or_create(
        name='upload_to_geonode',
        defaults={
            'func': 'geonode.geonode_updater.tasks.upload_to_geonode',
            'schedule_type': Schedule.MINUTES,
            'minutes': 10,
            'repeats': -1,
        }
    )
