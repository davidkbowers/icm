from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class work_timeListView(generic.ListView):
    model = models.work_time
    form_class = forms.work_timeForm


class work_timeCreateView(generic.CreateView):
    model = models.work_time
    form_class = forms.work_timeForm


class work_timeDetailView(generic.DetailView):
    model = models.work_time
    form_class = forms.work_timeForm


class work_timeUpdateView(generic.UpdateView):
    model = models.work_time
    form_class = forms.work_timeForm
    pk_url_kwarg = "pk"


class work_timeDeleteView(generic.DeleteView):
    model = models.work_time
    success_url = reverse_lazy("app_employee_work_time_list")
