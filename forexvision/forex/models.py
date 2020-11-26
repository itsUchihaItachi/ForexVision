from django.db import models

# Create your models here.
class forex_hours(models.Model):
    country_name = models.CharField(max_length=50)
    open_time = models.TextField()
    close_time = models.TextField()

class Trader(models.Model):
    Name = models.CharField(max_length=200)
    Region = models.CharField(max_length=200)
    Minimum_Deposit = models.IntegerField()
    Bank_Transfer =models.CharField(max_length=20)
    Withdrawl_Fee = models.CharField(max_length=20)
    Neg_Bal_Protection = models.CharField(max_length=20)
    Rating = models.IntegerField()
    Benefits = models.CharField(max_length=200)
    Platform_Setup = models.CharField(max_length=200)
    Accounts = models.CharField(max_length=200)

class Spread(models.Model):
    trader =models.ForeignKey(Trader, on_delete=models.CASCADE)
    INRUSD = models.FloatField ()
    INREUR = models.FloatField ()
    INRJPY = models.FloatField ()
    INRCAD = models.FloatField ()
    INRAUD = models.FloatField ()
