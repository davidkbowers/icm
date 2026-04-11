from django.urls import path
from . import views


urlpatterns = [
    path("timecard/", views.timecard, name="timecard"),
    path("app_employee/work_time/", views.work_timeListView.as_view(), name="app_employee_work_time_list"),
    path("app_employee/work_time/create/", views.work_timeCreateView.as_view(), name="app_employee_work_time_create"),
    path("app_employee/work_time/detail/<uuid:pk>/", views.work_timeDetailView.as_view(), name="app_employee_work_time_detail"),
    path("app_employee/work_time/update/<uuid:pk>/", views.work_timeUpdateView.as_view(), name="app_employee_work_time_update"),
    path("app_employee/work_time/delete/<uuid:pk>/", views.work_timeDeleteView.as_view(), name="app_employee_work_time_delete"),
]
