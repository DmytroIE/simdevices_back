import json
from rest_framework import serializers

from .models import Datastream
from django_celery_beat.models import PeriodicTask


class PeriodicTaskNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = ['interval', 'enabled']


class DatastreamSerializer(serializers.ModelSerializer):
    task = PeriodicTaskNestedSerializer()

    class Meta:
        model = Datastream
        fields = ['id', 'type', 'device', 'is_query_perm',
                  'val_max', 'val_min', 'task']
    
    def create(self, validated_data):
        task_data = validated_data.pop('task')
        datastream = Datastream.objects.create(**validated_data)
        task_name = f'd{datastream.device_id}-t{datastream.type_id}-{datastream.id}'
        task = None
        if task_data and ('enabled' in task_data) and ('interval' in task_data) and task_data['interval']:
            task = PeriodicTask.objects.create(
                    interval = task_data['interval'],
                    name = task_name, 
                    task='apps.readings.tasks.write_reading_to_db',
                    args=json.dumps([datastream.id, datastream.val_min, datastream.val_max]),
                    enabled = task_data['enabled']
                    )
        datastream.task = task
        datastream.save()
        return datastream
    
    def update(self, instance, validated_data):
        task_data = validated_data.pop('task')
        print(task_data)
        print(instance.task)
        print('interval' in task_data)
        ds_changed = False
        limits_changed = False
        for n in ['type', 'device', 'is_query_perm', 'val_max', 'val_min']:
            if getattr(instance, n) != validated_data[n]:
                setattr(instance, n, validated_data[n])
                ds_changed = True
                if n == 'val_max' or n == 'val_min':
                    limits_changed = True
        
        is_new_task_needed = False
        task_name = ''
        if (not instance.task) and task_data and ('enabled' in task_data) and ('interval' in task_data) and task_data['interval']:
            print('no task found in the ds, a new one is needed')
            is_new_task_needed = True
            task_name = f'd{instance.device_id}-t{instance.type_id}-{instance.id}'
        elif instance.task \
            and (limits_changed
            or
            (task_data and ('enabled' in task_data) and ('interval' in task_data) and task_data['interval'] and (instance.task.interval_id != task_data['interval'].id))):
            task_name = instance.task.name
            instance.task.enabled = False
            instance.task.save()
            instance.task.delete()
            is_new_task_needed = True
            print('task update is needed')

        if is_new_task_needed:
            task = PeriodicTask.objects.create(
                interval = task_data['interval'],
                name = task_name, 
                task='apps.readings.tasks.write_reading_to_db',
                args=json.dumps([instance.id, instance.val_min, instance.val_max]),
                enabled = task_data['enabled']
                )
            instance.task = task
            ds_changed = True
        elif task_data and ('enabled' in task_data)\
            and instance.task \
            and instance.task.enabled != task_data['enabled']:
            instance.task.enabled = task_data['enabled']
            instance.task.save()
        elif (not task_data) or (('interval' in task_data) and not task_data['interval']):
            if instance.task:
                t = instance.task
                instance.task = None
                t.enabled = False
                t.save()
                t.delete()
                ds_changed = True

            
        if ds_changed:
            instance.save()
            print('datastream saved')
        
        return instance



