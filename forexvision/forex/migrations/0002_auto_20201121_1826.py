# Generated by Django 3.0.8 on 2020-11-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forex_hours',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
