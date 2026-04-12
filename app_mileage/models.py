import uuid
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


class mileage_reimbursement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey("app_employees.employee", on_delete=models.CASCADE, related_name="mileage_reimbursements")
    week_start_date = models.DateField()
    mileage_date = models.DateField()
    purpose = models.CharField(max_length=120, blank=True)
    miles = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    job_number_phase_cat_desc = models.ForeignKey(
        "app_other.job_phase_cat_desc",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mileage_reimbursements",
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["mileage_date", "created"]

    def clean(self):
        if self.week_start_date and self.week_start_date.weekday() != 0:
            raise ValidationError({"week_start_date": "Week start date must be a Monday."})

        if self.week_start_date and self.mileage_date:
            week_end = self.week_start_date + timedelta(days=6)
            if not (self.week_start_date <= self.mileage_date <= week_end):
                raise ValidationError({"mileage_date": "Mileage date must be within the selected week."})

    def __str__(self):
        return f"{self.employee} {self.mileage_date} {self.miles} mi"


class auto_allowance_day(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allowance_date = models.DateField(unique=True)
    mileage_reimbursement_allowed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["allowance_date"]

    def __str__(self):
        return f"{self.allowance_date} allowed={self.mileage_reimbursement_allowed}"
