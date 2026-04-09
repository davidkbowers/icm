from django import forms
from . import models


class emp_typeForm(forms.ModelForm):
    class Meta:
        model = models.emp_type
        fields = [
            "name",
        ]


class employeeForm(forms.ModelForm):
    class Meta:
        model = models.employee
        fields = [
            "type",
            "has_truck",
            "name",
        ]
