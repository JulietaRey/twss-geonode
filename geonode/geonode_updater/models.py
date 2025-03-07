from django.db import models

class GeoJSONUpdateLog(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
