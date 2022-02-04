from django import forms


class SearchForm(forms.Form):
    vehicle_capacity = forms.MultipleChoiceField(['X', 'L', 'S', 'U'],
                                                 null=True)
    sum_passengers = forms.IntegerField(max_value = 10,
                                        min_value = 1,
                                        null=True)
    special_request_info = forms.CharField(max_length = 200,
                                           null=True)
