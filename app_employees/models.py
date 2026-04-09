from django.db import models
from django.urls import reverse


class emp_type(models.Model):

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=100)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("app_employee_emp_type_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_emp_type_update", args=(self.pk,))



class employee(models.Model):

    # Fields
    type = models.UUIDField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    has_truck = models.BooleanField()
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.TextField(max_length=100)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("app_employee_employee_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("app_employee_employee_update", args=(self.pk,))




