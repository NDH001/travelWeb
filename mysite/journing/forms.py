from django import forms
from traveldata.models import Cities


class NewJournalForm(forms.Form):
    where_to = forms.ModelChoiceField(
        queryset=Cities.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={"class": "city"}),
    )
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={"class": "start-date"})
    )
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={"class": "end-date"})
    )
