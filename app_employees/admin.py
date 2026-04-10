from django.contrib import admin
from django import forms

from . import models


class emp_tradeAdminForm(forms.ModelForm):

    class Meta:
        model = models.emp_trade
        fields = "__all__"


class emp_tradeAdmin(admin.ModelAdmin):
    form = emp_tradeAdminForm
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
        "trade",
        "id",
        "has_truck",
        "last_updated",
        "created",
        "name",
    ]
    readonly_fields = [
        "trade",
        "id",
        "has_truck",
        "last_updated",
        "created",
        "name",
    ]


admin.site.register(models.emp_trade, emp_tradeAdmin)
admin.site.register(models.employee, employeeAdmin)
