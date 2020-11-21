from django.db import models

# Create your models here.
class forex_hours(models.Model):
    country_name = models.CharField(max_length=50)
    open_time = models.TextField()
    close_time = models.TextField()
    status = models.BooleanField()

    