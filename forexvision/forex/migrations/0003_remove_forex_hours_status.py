# Generated by Django 3.0.8 on 2020-11-23 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '0002_auto_20201121_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forex_hours',
            name='status',
        ),
    ]