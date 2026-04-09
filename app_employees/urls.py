from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("emp_type", api.emp_typeViewSet)
router.register("employee", api.employeeViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("app_employee/emp_type/", views.emp_typeListView.as_view(), name="app_employee_emp_type_list"),
    path("app_employee/emp_type/create/", views.emp_typeCreateView.as_view(), name="app_employee_emp_type_create"),
    path("app_employee/emp_type/detail/<int:pk>/", views.emp_typeDetailView.as_view(), name="app_employee_emp_type_detail"),
    path("app_employee/emp_type/update/<int:pk>/", views.emp_typeUpdateView.as_view(), name="app_employee_emp_type_update"),
    path("app_employee/emp_type/delete/<int:pk>/", views.emp_typeDeleteView.as_view(), name="app_employee_emp_type_delete"),
    path("app_employee/employee/", views.employeeListView.as_view(), name="app_employee_employee_list"),
    path("app_employee/employee/create/", views.employeeCreateView.as_view(), name="app_employee_employee_create"),
    path("app_employee/employee/detail/<int:pk>/", views.employeeDetailView.as_view(), name="app_employee_employee_detail"),
    path("app_employee/employee/update/<int:pk>/", views.employeeUpdateView.as_view(), name="app_employee_employee_update"),
    path("app_employee/employee/delete/<int:pk>/", views.employeeDeleteView.as_view(), name="app_employee_employee_delete"),
)
