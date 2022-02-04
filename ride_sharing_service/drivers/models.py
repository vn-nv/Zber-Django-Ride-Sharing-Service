from django.db import models
from django.contrib.auth.models import User
import sys
sys.path.append("..")
from zber.models import VEHICLE_TYPES


class Driver(models.Model):
    driver_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_license = models.CharField(max_length=9)
    vehicle_type = models.CharField(max_length=1, choices=VEHICLE_TYPES)
    VIN = models.CharField(max_length=17)
    license_plate = models.CharField(max_length=10)
    max_passengers = models.IntegerField()
    special_info = models.CharField(max_length=200, null=True)

