from django.urls import path

from . import views

urlpatterns = [
    path('timesheet/', views.timecard, name='timecard'),
]
