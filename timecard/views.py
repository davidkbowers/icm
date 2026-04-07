from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Phase


@login_required
def timecard(request):
	phases = list(
		Phase.objects.filter(is_active=True)
		.order_by("code")
		.values("id", "code", "name")
	)
	return render(request, "timecard/timesheet.html", {"phases": phases})
