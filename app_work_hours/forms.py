from django import forms
from django.utils import timezone
from app_employees.models import employee
from app_other.models import job_phase_cat_desc
from . import models


class work_timeForm(forms.ModelForm):
    class Meta:
        model = models.work_time
        fields = [
            "work_type",
            "hours_worked",
            "rate_modifier",
            "job_number_phase_cat_desc",
            "work_date",
        ]


class WeeklyTimecardForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=employee.objects.all(),
        empty_label="Select employee",
        label="Employee",
    )
    week_start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Week start (Monday)",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["employee"].queryset = self.fields["employee"].queryset.order_by("name")
        self.fields["week_start_date"].initial = timezone.localdate()

    def clean_week_start_date(self):
        week_start = self.cleaned_data["week_start_date"]
        if week_start.weekday() != 0:
            raise forms.ValidationError("Please choose a Monday for the week start date.")
        return week_start


class TimecardRowForm(forms.Form):
    job_number_phase_cat_desc = forms.ModelChoiceField(
        queryset=job_phase_cat_desc.objects.all(),
        empty_label="Select job number, phase, category & description",
        label="Job Number, Phase, Category & Description",
    )

    mon = forms.IntegerField(min_value=0, max_value=24, required=False, initial=0)
    tue = forms.IntegerField(min_value=0, max_value=24, required=False, initial=0)
    wed = forms.IntegerField(min_value=0, max_value=24, required=False, initial=0)
    thu = forms.IntegerField(min_value=0, max_value=24, required=False, initial=0)
    fri = forms.IntegerField(min_value=0, max_value=24, required=False, initial=0)
    sat = forms.IntegerField(min_value=0, max_value=24, required=False, initial=0)
    sun = forms.IntegerField(min_value=0, max_value=24, required=False, initial=0)

    day_field_map = {
        0: "mon",
        1: "tue",
        2: "wed",
        3: "thu",
        4: "fri",
        5: "sat",
        6: "sun",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job_number_phase_cat_desc"].queryset = self.fields["job_number_phase_cat_desc"].queryset.order_by("item")
        self.fields["job_number_phase_cat_desc"].label_from_instance = lambda obj: obj.item

    def clean(self):
        cleaned_data = super().clean()
        for day_field in self.day_field_map.values():
            cleaned_data[day_field] = cleaned_data.get(day_field) or 0
        return cleaned_data
