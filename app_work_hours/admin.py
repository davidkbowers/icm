from django.contrib import admin
from django import forms

from . import models


class work_timeAdminForm(forms.ModelForm):

    class Meta:
        model = models.work_time
        fields = "__all__"


class work_timeAdmin(admin.ModelAdmin):
    form = work_timeAdminForm
    list_display = [
        "id",
        "employee_id",
        "work_type",
        "hours_worked",
        "rate_modifier",
        "job_number_phase_cat_desc",
        "work_date",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "id",
        "employee_id",
        "work_type",
        "hours_worked",
        "rate_modifier",
        "job_number_phase_cat_desc",
        "work_date",
        "created",
        "last_updated",
    ]


admin.site.register(models.work_time, work_timeAdmin)
