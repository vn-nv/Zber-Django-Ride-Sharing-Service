from django import forms
from django.forms.models import inlineformset_factory
from .models import Driver
import sys
sys.path.append("..")
from riders.models import Ride, Ride_Owner
from zber.models import VEHICLE_TYPES

"""
   Form of registering a user
"""


class DriverForm(forms.ModelForm):
    special_info = forms.CharField(required=False, max_length=200)
    class Meta:
        model = Driver
        exclude = ['user', 'driver_id']
        widgets = {
        }


class SearchForm(forms.Form):
    max_passengers = forms.IntegerField(required=False)
    vehicle_type = forms.MultipleChoiceField(choices=VEHICLE_TYPES, required=False)
    special_request_info = forms.CharField(max_length=200, required=False)

        
SearchFormSet = inlineformset_factory(Ride_Owner,
                                      Ride,
                                      fields = ('sum_passengers',),
                                      extra = 1)
