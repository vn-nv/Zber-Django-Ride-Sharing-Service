from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User


"""
   Form of registering a user
"""


class LogupForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': PasswordInput(),
        }
