from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import EmailAuthenticationForm, RegistrationForm


def home(request):
    if request.user.is_authenticated:
        return redirect("timecard")

    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("timecard")

    return render(request, "users/home.html", {"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect("timecard")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            user = form.save()
        except ValidationError as exc:
            form.add_error("email", str(exc))
        else:
            login(request, user)
            return redirect("timecard")

    return render(request, "users/register.html", {"form": form})
