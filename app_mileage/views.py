from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import redirect, render

from app_employees.models import employee

from . import forms, models


def _display_week_start(weekly_form):
    raw_value = weekly_form["week_start_date"].value()
    try:
        week_start = date.fromisoformat(str(raw_value))
    except (TypeError, ValueError):
        return date.today() - timedelta(days=date.today().weekday())
    return week_start - timedelta(days=week_start.weekday())


@login_required
def mileage_reimbursement(request):
    RowFormSet = formset_factory(forms.MileageRowForm, extra=1, can_delete=True)

    form = forms.WeeklyMileageForm(request.POST or None)
    row_formset = RowFormSet(request.POST or None, prefix="rows")
    total_miles = 0
    total_amount = 0

    if request.method == "POST" and form.is_valid() and row_formset.is_valid():
        selected_employee = form.cleaned_data["employee"]
        week_start = form.cleaned_data["week_start_date"]
        week_end = week_start + timedelta(days=6)

        models.mileage_reimbursement.objects.filter(
            employee=selected_employee,
            mileage_date__range=(week_start, week_end),
        ).delete()

        for row_form in row_formset:
            row_data = row_form.cleaned_data
            if not row_data or row_data.get("DELETE"):
                continue

            mileage_date = row_data.get("mileage_date")
            if not mileage_date:
                continue

            models.mileage_reimbursement.objects.create(
                employee=selected_employee,
                week_start_date=week_start,
                mileage_date=mileage_date,
                purpose=row_data.get("purpose") or "",
                miles=row_data.get("miles") or 0,
                amount=row_data.get("amount") or 0,
                job_number_phase_cat_desc=row_data.get("job_number_phase_cat_desc"),
            )

        return redirect(f"{request.path}?employee={selected_employee.id}&week_start_date={week_start}")

    if request.method == "GET":
        employee_id = request.GET.get("employee")
        week_start_raw = request.GET.get("week_start_date")
        if employee_id and week_start_raw:
            try:
                selected_employee = form.fields["employee"].queryset.get(pk=employee_id)
                week_start = date.fromisoformat(week_start_raw)
            except (ValueError, TypeError, employee.DoesNotExist):
                selected_employee = None
                week_start = None

            if selected_employee and week_start and week_start.weekday() == 0:
                week_end = week_start + timedelta(days=6)
                entries = models.mileage_reimbursement.objects.filter(
                    employee=selected_employee,
                    mileage_date__range=(week_start, week_end),
                ).order_by("mileage_date")

                initial_rows = []
                for entry in entries:
                    initial_rows.append(
                        {
                            "mileage_date": entry.mileage_date,
                            "purpose": entry.purpose,
                            "miles": entry.miles,
                            "amount": entry.amount,
                            "job_number_phase_cat_desc": entry.job_number_phase_cat_desc,
                        }
                    )
                    total_miles += float(entry.miles)
                    total_amount += float(entry.amount)

                form = forms.WeeklyMileageForm(initial={"employee": selected_employee, "week_start_date": week_start})
                row_formset = RowFormSet(initial=initial_rows or None, prefix="rows")

    display_week_start = _display_week_start(form)
    period_ending = display_week_start + timedelta(days=6)

    return render(
        request,
        "app_mileage/mileage_reimbursement.html",
        {
            "form": form,
            "row_formset": row_formset,
            "total_miles": f"{total_miles:.2f}",
            "total_amount": f"{total_amount:.2f}",
            "period_ending": f"{period_ending.month}/{period_ending.day}/{period_ending.year}",
        },
    )
