from django.db import models
from django.urls import reverse


class work_time(models.Model):

    # Fields
    work_type = models.IntegerField()
    hours_worked = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    day_of_week = models.IntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_number = models.TextField(max_length=100)
    job_description = models.TextField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    job_phase = models.TextField(max_length=100)
    job_category = models.TextField(max_length=100)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("app_employee_work_time_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_work_time_update", args=(self.pk,))

