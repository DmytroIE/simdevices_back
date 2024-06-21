import datetime
import json
import django.db
from django.db import models
from django_celery_beat.models import PeriodicTask
from apps.devices.models import Device

class DatastreamType(models.Model):
    class Meta:
        db_table = "dstypes"

    name = models.CharField(max_length=200, blank = False, unique = True)

    def __str__(self):
        return self.name

def SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT(collector, field, sub_objs, using):
# https://stackoverflow.com/questions/48322538/django-foreignkey-on-delete-set-default-behavior
    try:
        default_dstype = DatastreamType.objects.get(name='Unknown')
    except DatastreamType.DoesNotExist:
        raise django.db.InternalError("You should have default DatastreamType=Unknown before "
                                      "deleting a referenced DatastreamType")
    for item in sub_objs:
        if item.type == default_dstype:
            raise django.db.InternalError("You cannot delete default DatastreamType "
                                          "when there are items referencing it")

    collector.add_field_update(field, default_dstype, sub_objs)



class Datastream(models.Model):

    class Meta:
        db_table = "datastreams"

    type = models.ForeignKey(
        DatastreamType,
        on_delete = SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT,
    )

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
    )
    
    task = models.OneToOneField(PeriodicTask, 
                             on_delete = models.SET_NULL,
                             null = True,
                             blank = True,
                             default = None)

    is_query_perm = models.BooleanField(default = True)  # if True then the external consumer can query
    val_max = models.FloatField()
    val_min = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Datastream dev_id:{self.device.id} id:{self.id}'
    
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         print(f'self id before saving = {self.id}')
    #         super().save(*args, **kwargs) # save a datastream without a task to get an id
    #         print(f'self id after saving = {self.id}')
    #     task_name = f'd{self.device_id}-t{self.type_id}-{self.id}'
    #     task_obj = DsPeriodicTask.objects.filter(name=task_name).first()
    #     if task_obj:
    #         # if the task exists then it is not possible to change here anything but "enabled"
    #         print('Task exists, just needs updating')
    #         if task_obj.enabled != self.is_sim_active:
    #             task_obj.enabled = self.is_sim_active
    #             task_obj.save()
    #     else:
    #         print('No task assigned, so create a task')
    #         interval = IntervalSchedule.objects.filter(pk=self.interval_id).get()

    #         self.task = DsPeriodicTask.objects.create(
    #             interval = interval,
    #             name = task_name, 
    #             task='apps.readings.tasks.write_reading_to_db',
    #             args=json.dumps([self.id, self.val_min, self.val_max]),
    #             enabled = self.is_sim_active
    #             )


    
    # def delete(self, *args, **kwargs):
    #     print('datastream delete - before')
    #     if self.task:
    #         self.task.delete()
    #     print('datastream delete - after')
    #     super().delete(*args, **kwargs)
