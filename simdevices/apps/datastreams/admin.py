from django.contrib import admin
from .models import Datastream, DatastreamType

admin.site.register(Datastream)
admin.site.register(DatastreamType)
