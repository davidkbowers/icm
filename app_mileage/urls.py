from django.urls import path

from . import views

urlpatterns = [
    path("mileage/", views.mileage_reimbursement, name="mileage_reimbursement"),
]
