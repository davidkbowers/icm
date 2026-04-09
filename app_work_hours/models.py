from django.db import models
from django.urls import reverse


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

