from django import forms
from traveldata.models import Cities
from datetime import datetime


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

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data["start_date"]
        end = cleaned_data["end_date"]

        if end < start:
            raise forms.ValidationError("Invalid Dates!")
