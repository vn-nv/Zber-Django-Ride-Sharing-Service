from django import forms


class SearchForm(forms.Form):
    num_passengers = forms.IntegerField(null=False)
    destination = forms.CharField(null=False)
    early_arrival_time = forms.DateTimeField(null=False)
    late_arrival_time = forms.DateTimeField(null=False)
