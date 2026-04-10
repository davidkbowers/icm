from django.contrib import admin

from . import models


class JobPhaseCatDescAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "work_type",
        "item",
    ]


class RateModifierAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "acronym",
        "description",
    ]
    readonly_fields = [
        "id",
    ]


admin.site.register(models.job_phase_cat_desc, JobPhaseCatDescAdmin)
admin.site.register(models.RateModifier, RateModifierAdmin)
