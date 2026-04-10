from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("emp_trade", api.emp_tradeViewSet)
router.register("employee", api.employeeViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("app_employee/emp_trade/", views.emp_tradeListView.as_view(), name="app_employee_emp_trade_list"),
    path("app_employee/emp_trade/create/", views.emp_tradeCreateView.as_view(), name="app_employee_emp_trade_create"),
    path("app_employee/emp_trade/detail/<int:pk>/", views.emp_tradeDetailView.as_view(), name="app_employee_emp_trade_detail"),
    path("app_employee/emp_trade/update/<int:pk>/", views.emp_tradeUpdateView.as_view(), name="app_employee_emp_trade_update"),
    path("app_employee/emp_trade/delete/<int:pk>/", views.emp_tradeDeleteView.as_view(), name="app_employee_emp_trade_delete"),
    path("app_employee/employee/", views.employeeListView.as_view(), name="app_employee_employee_list"),
    path("app_employee/employee/create/", views.employeeCreateView.as_view(), name="app_employee_employee_create"),
    path("app_employee/employee/detail/<int:pk>/", views.employeeDetailView.as_view(), name="app_employee_employee_detail"),
    path("app_employee/employee/update/<int:pk>/", views.employeeUpdateView.as_view(), name="app_employee_employee_update"),
    path("app_employee/employee/delete/<int:pk>/", views.employeeDeleteView.as_view(), name="app_employee_employee_delete"),
)
