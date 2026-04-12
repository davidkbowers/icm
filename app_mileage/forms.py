from django import forms
from django.utils import timezone

from app_employees.models import employee
from app_other.models import job_phase_cat_desc


class WeeklyMileageForm(forms.Form):
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
        today = timezone.localdate()
        self.fields["week_start_date"].initial = today

    def clean_week_start_date(self):
        week_start = self.cleaned_data["week_start_date"]
        if week_start.weekday() != 0:
            raise forms.ValidationError("Please choose a Monday for the week start date.")
        return week_start


class MileageRowForm(forms.Form):
    mileage_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date",
    )
    purpose = forms.CharField(required=False, max_length=120, label="Purpose")
    miles = forms.DecimalField(required=False, min_value=0, max_digits=7, decimal_places=2, initial=0, label="Miles")
    amount = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2, initial=0, label="Amount")
    job_number_phase_cat_desc = forms.ModelChoiceField(
        queryset=job_phase_cat_desc.objects.all(),
        required=False,
        empty_label="-",
        label="Job",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job_number_phase_cat_desc"].queryset = self.fields["job_number_phase_cat_desc"].queryset.order_by("item")
        self.fields["job_number_phase_cat_desc"].label_from_instance = lambda obj: obj.item

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["miles"] = cleaned_data.get("miles") or 0
        cleaned_data["amount"] = cleaned_data.get("amount") or 0

        has_data = any(
            [
                cleaned_data.get("mileage_date"),
                cleaned_data.get("purpose"),
                cleaned_data.get("job_number_phase_cat_desc"),
                cleaned_data.get("miles"),
                cleaned_data.get("amount"),
            ]
        )
        if has_data and not cleaned_data.get("mileage_date"):
            self.add_error("mileage_date", "Date is required when entering mileage data.")
        return cleaned_data
