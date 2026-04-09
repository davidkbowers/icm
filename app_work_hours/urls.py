from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("work_time", api.work_timeViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("app_employee/work_time/", views.work_timeListView.as_view(), name="app_employee_work_time_list"),
    path("app_employee/work_time/create/", views.work_timeCreateView.as_view(), name="app_employee_work_time_create"),
    path("app_employee/work_time/detail/<int:pk>/", views.work_timeDetailView.as_view(), name="app_employee_work_time_detail"),
    path("app_employee/work_time/update/<int:pk>/", views.work_timeUpdateView.as_view(), name="app_employee_work_time_update"),
    path("app_employee/work_time/delete/<int:pk>/", views.work_timeDeleteView.as_view(), name="app_employee_work_time_delete"),

)
