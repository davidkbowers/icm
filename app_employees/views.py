from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class emp_typeListView(generic.ListView):
    model = models.emp_type
    form_class = forms.emp_typeForm


class emp_typeCreateView(generic.CreateView):
    model = models.emp_type
    form_class = forms.emp_typeForm


class emp_typeDetailView(generic.DetailView):
    model = models.emp_type
    form_class = forms.emp_typeForm


class emp_typeUpdateView(generic.UpdateView):
    model = models.emp_type
    form_class = forms.emp_typeForm
    pk_url_kwarg = "pk"


class emp_typeDeleteView(generic.DeleteView):
    model = models.emp_type
    success_url = reverse_lazy("app_employee_emp_type_list")


class employeeListView(generic.ListView):
    model = models.employee
    form_class = forms.employeeForm


class employeeCreateView(generic.CreateView):
    model = models.employee
    form_class = forms.employeeForm


class employeeDetailView(generic.DetailView):
    model = models.employee
    form_class = forms.employeeForm


class employeeUpdateView(generic.UpdateView):
    model = models.employee
    form_class = forms.employeeForm
    pk_url_kwarg = "pk"


class employeeDeleteView(generic.DeleteView):
    model = models.employee
    success_url = reverse_lazy("app_employee_employee_list")
