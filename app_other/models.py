from django.db import models
from django.urls import reverse


class work_time(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)work_type = models.IntegerField()
    work_date = models.DateField()
    hours_worked = models.IntegerField()
    hours_type = models.CharField(max_length=2)
    day_of_week = models.IntegerField()
    job_number = models.TextField(max_length=100)
    job_description = models.TextField(max_length=100)
    job_phase = models.TextField(max_length=100)
    job_category = models.TextField(max_length=100)
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

