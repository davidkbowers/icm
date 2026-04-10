from django.db import models
from django.urls import reverse
import uuid


class emp_trade(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acronym = models.CharField(max_length=15)
    name = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("app_employee_emp_trade_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_emp_trade_update", args=(self.pk,))



class employee(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=100)
    trade = models.ForeignKey("emp_trade", on_delete=models.SET_NULL, null=True, blank=True)
    has_truck = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("app_employee_employee_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_employee_update", args=(self.pk,))




