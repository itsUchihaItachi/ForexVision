from django.db import models

# Create your models here
class market_time(models.Model):
    country_name = models.CharField(max_length=50)
    open_time = models.TimeField(auto_now=False, auto_now_add=False)
    close_time = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.BooleanField()

    def __str__(self):
        return self.country_name
