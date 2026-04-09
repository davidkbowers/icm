from django import forms
from . import models


class work_timeForm(forms.ModelForm):
    class Meta:
        model = models.work_time
        fields = [
            "work_type",
            "hours_worked",
            "day_of_week",
            "job_number",
            "job_description",
            "job_phase",
            "job_category",
        ]
