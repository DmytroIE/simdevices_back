# Generated by Django 5.0.6 on 2024-06-20 22:10

import apps.datastreams.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0001_initial'),
        ('django_celery_beat', '0018_improve_crontab_helptext'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatastreamType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'dstypes',
            },
        ),
        migrations.CreateModel(
            name='Datastream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_query_perm', models.BooleanField(default=True)),
                ('val_max', models.FloatField()),
                ('val_min', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.device')),
                ('task', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_beat.periodictask')),
                ('type', models.ForeignKey(on_delete=apps.datastreams.models.SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT, to='datastreams.datastreamtype')),
            ],
            options={
                'db_table': 'datastreams',
            },
        ),
    ]
