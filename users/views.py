from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import EmailAuthenticationForm


def home(request):
	if request.user.is_authenticated:
		return redirect("timesheet")

	form = EmailAuthenticationForm(request, data=request.POST or None)
	if request.method == "POST" and form.is_valid():
		login(request, form.get_user())
		return redirect("timesheet")

	return render(request, "users/home.html", {"form": form})


@login_required
def timesheet(request):
	return render(request, "users/timesheet.html")
