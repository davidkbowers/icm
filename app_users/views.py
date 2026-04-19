from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import EmailAuthenticationForm


def home(request):
    if request.user.is_authenticated:
        return redirect("timecard")

    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("timecard")

    return render(request, "users/home.html", {"form": form})
