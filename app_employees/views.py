from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class emp_tradeListView(generic.ListView):
    model = models.emp_trade
    form_class = forms.emp_tradeForm


class emp_tradeCreateView(generic.CreateView):
    model = models.emp_trade
    form_class = forms.emp_tradeForm


class emp_tradeDetailView(generic.DetailView):
    model = models.emp_trade
    form_class = forms.emp_tradeForm


class emp_tradeUpdateView(generic.UpdateView):
    model = models.emp_trade
    form_class = forms.emp_tradeForm
    pk_url_kwarg = "pk"


class emp_tradeDeleteView(generic.DeleteView):
    model = models.emp_trade
    success_url = reverse_lazy("app_employee_emp_trade_list")


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
