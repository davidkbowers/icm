from django.contrib import admin

from .models import auto_allowance_day, mileage_reimbursement


@admin.register(mileage_reimbursement)
class MileageReimbursementAdmin(admin.ModelAdmin):
    list_display = ("employee", "mileage_date", "miles", "amount", "job_number_phase_cat_desc")
    list_filter = ("employee", "week_start_date", "mileage_date")
    search_fields = ("employee__name", "purpose", "job_number_phase_cat_desc__item")


@admin.register(auto_allowance_day)
class AutoAllowanceDayAdmin(admin.ModelAdmin):
    list_display = ("allowance_date", "mileage_reimbursement_allowed")
    list_filter = ("mileage_reimbursement_allowed",)
    search_fields = ("allowance_date",)
