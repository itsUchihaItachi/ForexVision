from django.db import models

# Create your models here.
class Trader(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    minDeposit = models.IntegerField()
    bankTransfer =models.CharField(max_length=20)
    withdrawlFee = models.CharField(max_length=20)
    negBalProtection = models.CharField(max_length=20)
    rating = models.IntegerField()
    benefit = models.CharField(max_length=200)
    platformSup = models.CharField(max_length=200)
    accounts = models.CharField(max_length=200)



class Spread(models.Model):
    trader =models.ForeignKey(Trader, on_delete=models.CASCADE)
    INRUSD = models.FloatField ()
    INREUR = models.FloatField ()
    INRJPY = models.FloatField ()
    INRCAD = models.FloatField ()
    INRAUD = models.FloatField ()