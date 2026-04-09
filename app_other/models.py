from django.db import models
from django.urls import reverse


class job_phase_cat_desc(models.Model):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)work_type = models.IntegerField()
    item = models.TextField(max_length=100)
    
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("app_employee_work_time_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_work_time_update", args=(self.pk,))

