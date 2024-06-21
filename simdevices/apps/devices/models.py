from django.db import models


class Device(models.Model):
    class Meta:
        db_table = "devices"

    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device {self.name} id:{self.id}"