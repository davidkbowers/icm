from django.contrib import admin
from django import forms

from . import models


class emp_typeAdminForm(forms.ModelForm):

    class Meta:
        model = models.emp_type
        fields = "__all__"


class emp_typeAdmin(admin.ModelAdmin):
    form = emp_typeAdminForm
    list_display = [
        "last_updated",
        "created",
        "id",
        "name",
    ]
    readonly_fields = [
        "last_updated",
        "created",
        "id",
        "name",
    ]


class employeeAdminForm(forms.ModelForm):

    class Meta:
        model = models.employee
        fields = "__all__"


class employeeAdmin(admin.ModelAdmin):
    form = employeeAdminForm
    list_display = [
        "type",
        "id",
        "has_truck",
        "last_updated",
        "created",
        "name",
    ]
    readonly_fields = [
        "type",
        "id",
        "has_truck",
        "last_updated",
        "created",
        "name",
    ]


class work_timeAdminForm(forms.ModelForm):

    class Meta:
        model = models.work_time
        fields = "__all__"


class work_timeAdmin(admin.ModelAdmin):
    form = work_timeAdminForm
    list_display = [
        "work_type",
        "hours_worked",
        "created",
        "day_of_week",
        "id",
        "job_number",
        "job_description",
        "last_updated",
        "job_phase",
        "job_category",
    ]
    readonly_fields = [
        "work_type",
        "hours_worked",
        "created",
        "day_of_week",
        "id",
        "job_number",
        "job_description",
        "last_updated",
        "job_phase",
        "job_category",
    ]


admin.site.register(models.emp_type, emp_typeAdmin)
admin.site.register(models.employee, employeeAdmin)
admin.site.register(models.work_time, work_timeAdmin)
