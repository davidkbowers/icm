from django.contrib import admin
from .models import Phase


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
	list_display = ("code", "name", "is_active")
	search_fields = ("code", "name")
	list_filter = ("is_active",)
