from django import forms
from django.forms.models import inlineformset_factory
from drivers.models import Driver
import sys
sys.path.append("..")
from .models import Ride, Ride_Owner, Ride_Sharer, User

"""
   Form of registering a user
"""

VEHICLE_TYPES = (
    ('', 'Any type'),
    ('X', 'zberX'),
    ('L', 'zberXL'),
    ('S', 'zberSUV'),
    ('U', 'zberLUX')
    )

NUM_SHARERS = (
    (1, 'One'),
    (2, 'Two'),
    (3, 'Three'),
    (4, 'Four'),
    (5, 'Five')
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ('dest_addr', 'arrival_time', 'share')
        widgets = {
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ('user',)

class RideOwnerForm(forms.ModelForm):
    specific_type = forms.ChoiceField(required=False, choices=VEHICLE_TYPES)
    special_requests = forms.CharField(required=False, max_length=200)
    class Meta:
        model = Ride_Owner
        exclude = ('order_no', 'user')


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ('ride_owner', 'driver', 'status',)


class SharerForm(forms.ModelForm):
    class Meta:
        model = Ride_Sharer
        fields = ('__all__')

