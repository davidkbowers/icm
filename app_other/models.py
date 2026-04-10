from django.db import models
from django.urls import reverse
import uuid


class job_phase_cat_desc(models.Model):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_type = models.IntegerField()
    item = models.TextField(max_length=100)
    
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("app_employee_work_time_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_work_time_update", args=(self.pk,))


class RateModifier(models.Model):
    id = models.AutoField(primary_key=True)
    acronym = models.CharField(max_length=15)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.acronym

