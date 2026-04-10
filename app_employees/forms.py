from django import forms
from . import models


class emp_tradeForm(forms.ModelForm):
    class Meta:
        model = models.emp_trade
        fields = [
            "name",
        ]


class employeeForm(forms.ModelForm):
    class Meta:
        model = models.employee
        fields = [
            "trade",
            "has_truck",
            "name",
        ]
