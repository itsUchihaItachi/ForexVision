# Generated by Django 3.1.3 on 2020-11-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country_time', '0004_auto_20201120_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market_time',
            name='close_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='market_time',
            name='open_time',
            field=models.TimeField(),
        ),
    ]
