from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def timecard(request):
	return render(request, 'timecard/timesheet.html')
