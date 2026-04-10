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


class time_cardAdminForm(forms.ModelForm):

    class Meta:
        model = models.time_card
        fields = "__all__"


class time_cardAdmin(admin.ModelAdmin):
    form = time_cardAdminForm
    list_display = [
        "id",
        "week_start_date",
        "week_end_date",
        "job_number_phase_cat_desc",
        "rate_modifier",
        "created",
        "last_updated",
    ]
    list_filter = [
        "week_start_date",
        "week_end_date",
        "job_number_phase_cat_desc",
        "rate_modifier",
    ]
    search_fields = [
        "job_number_phase_cat_desc__item",
        "rate_modifier__acronym",
        "employees__name",
    ]
    filter_horizontal = ["employees"]
    readonly_fields = [
        "id",
        "created",
        "last_updated",
    ]


admin.site.register(models.time_card, time_cardAdmin)
