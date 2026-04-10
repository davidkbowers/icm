from django.db import models
from django.urls import reverse
import uuid
from datetime import timedelta
from django.core.exceptions import ValidationError


class work_time(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.UUIDField(default=uuid.uuid4, editable=False)
    hours_worked = models.IntegerField()
    work_type = models.IntegerField()   # ST, OT, DT
    rate_modifier = models.FloatField() # 1.0, 1.5, 2.0
    job_number_phase_cat_desc = models.TextField(max_length=100) # D25746.01.03005.Misc. Concrete Field Labor			
    work_date = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
 
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("app_employee_work_time_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_work_time_update", args=(self.pk,))


class time_card(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employees = models.ManyToManyField("app_employees.employee", related_name="time_cards")
    job_number_phase_cat_desc = models.ForeignKey("app_other.job_phase_cat_desc", on_delete=models.PROTECT)
    rate_modifier = models.ForeignKey("app_other.RateModifier", on_delete=models.PROTECT)
    week_start_date = models.DateField()
    week_end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "week_start_date",
                    "week_end_date",
                    "job_number_phase_cat_desc",
                    "rate_modifier",
                ],
                name="uq_time_card_week_job_rate",
            )
        ]

    def clean(self):
        if self.week_start_date and self.week_start_date.weekday() != 0:
            raise ValidationError({"week_start_date": "Week start date must be a Monday."})

        if self.week_end_date and self.week_end_date.weekday() != 6:
            raise ValidationError({"week_end_date": "Week end date must be a Sunday."})

        if self.week_start_date and self.week_end_date:
            expected_end = self.week_start_date + timedelta(days=6)
            if self.week_end_date != expected_end:
                raise ValidationError({"week_end_date": "Week end date must be 6 days after week start date."})

    def __str__(self):
        return f"Time Card {self.week_start_date} - {self.week_end_date}"

