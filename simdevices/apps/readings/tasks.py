import random
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import Reading
from ..datastreams.models import Datastream


@shared_task
def write_reading_to_db(datastream_id, 
                        val_min, val_max):

    now = timezone.now()

    # simulate receiving the data from external_db/raw_readings
    sim_reading = val_min + (val_max-val_min) * random.random()
    timestamp = now - timedelta(milliseconds=random.randint(50, 250))

    # simulate writing in the db
    print(f'{datastream_id}: {timestamp}: {sim_reading}')
    ds = Datastream.objects.filter(pk=datastream_id).first()
    r = Reading(datastream = ds, timestamp = timestamp, reading = sim_reading)
    r.save()
