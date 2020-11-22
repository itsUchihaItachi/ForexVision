# Generated by Django 3.0.8 on 2020-11-21 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='forex_hours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=50)),
                ('open_time', models.TextField()),
                ('close_time', models.TextField()),
                ('status', models.BooleanField()),
            ],
        ),
    ]
