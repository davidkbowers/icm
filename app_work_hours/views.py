from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from app_employees.models import employee
from app_mileage import forms as mileage_forms
from app_mileage import models as mileage_models
from app_other.models import job_phase_cat_desc
from . import models
from . import forms


def _date_to_work_date_int(value):
    return int(value.strftime("%Y%m%d"))


def _display_week_start(weekly_form):
    raw_value = weekly_form["week_start_date"].value()
    try:
        week_start = date.fromisoformat(str(raw_value))
    except (TypeError, ValueError):
        week_start = timezone.localdate()
    return week_start - timedelta(days=week_start.weekday())


def _display_employee_name(weekly_form):
    employee_value = weekly_form["employee"].value()
    if not employee_value:
        return "-"
    selected = employee.objects.filter(pk=employee_value).first()
    return selected.name if selected else "-"


def _short_date(value):
    return f"{value.month}/{value.day}"


@login_required
def timecard(request):
    RowFormSet = formset_factory(forms.TimecardRowForm, extra=1, can_delete=True)
    MileageRowFormSet = formset_factory(mileage_forms.MileageRowForm, extra=2, can_delete=True)

    form = forms.WeeklyTimecardForm(request.POST or None)
    row_formset = RowFormSet(request.POST or None, prefix="rows")
    mileage_row_formset = MileageRowFormSet(request.POST or None, prefix="mileage_rows")
    day_fields = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    daily_totals = {day: 0 for day in day_fields}
    auto_allowance = {day: False for day in day_fields}
    week_total = 0
    mileage_total_miles = 0
    mileage_total_amount = 0

    if request.method == "POST":
        auto_allowance = {
            day: request.POST.get(f"auto_allowance_{day}") == "on"
            for day in day_fields
        }

    if request.method == "POST" and form.is_valid() and row_formset.is_valid() and mileage_row_formset.is_valid():
        selected_employee = form.cleaned_data["employee"]
        week_start = form.cleaned_data["week_start_date"]
        week_end = week_start + timedelta(days=6)
        week_dates = [week_start + timedelta(days=offset) for offset in range(7)]
        work_date_ints = [_date_to_work_date_int(day) for day in week_dates]

        models.work_time.objects.filter(
            employee_id=selected_employee.id,
            work_date__in=work_date_ints,
        ).delete()

        for row_form in row_formset:
            row_data = row_form.cleaned_data
            if not row_data or row_data.get("DELETE"):
                continue

            selected_job = row_data.get("job_number_phase_cat_desc")
            if not selected_job:
                continue

            for offset, day_name in enumerate(day_fields):
                hours = int(row_data.get(day_name) or 0)
                if hours <= 0:
                    continue
                models.work_time.objects.create(
                    employee_id=selected_employee.id,
                    work_type=1,
                    hours_worked=hours,
                    rate_modifier=1.0,
                    job_number_phase_cat_desc=selected_job.item,
                    work_date=work_date_ints[offset],
                )

        mileage_models.mileage_reimbursement.objects.filter(
            employee=selected_employee,
            mileage_date__range=(week_start, week_end),
        ).delete()

        for mileage_form in mileage_row_formset:
            mileage_data = mileage_form.cleaned_data
            if not mileage_data or mileage_data.get("DELETE"):
                continue

            mileage_date = mileage_data.get("mileage_date")
            if not mileage_date:
                continue

            mileage_models.mileage_reimbursement.objects.create(
                employee=selected_employee,
                week_start_date=week_start,
                mileage_date=mileage_date,
                purpose=mileage_data.get("purpose") or "",
                miles=mileage_data.get("miles") or 0,
                amount=mileage_data.get("amount") or 0,
                job_number_phase_cat_desc=mileage_data.get("job_number_phase_cat_desc"),
            )

        for index, day_name in enumerate(day_fields):
            mileage_models.auto_allowance_day.objects.update_or_create(
                allowance_date=week_dates[index],
                defaults={"mileage_reimbursement_allowed": auto_allowance[day_name]},
            )

        return redirect(f"{request.path}?employee={selected_employee.id}&week_start_date={week_start}")

    if request.method == "GET":
        employee_id = request.GET.get("employee")
        week_start_raw = request.GET.get("week_start_date")
        if employee_id and week_start_raw:
            selected_employee = None
            week_start = None
            try:
                selected_employee = form.fields["employee"].queryset.get(pk=employee_id)
                week_start = date.fromisoformat(week_start_raw)
            except (ValueError, TypeError, employee.DoesNotExist):
                selected_employee = None
                week_start = None

            if selected_employee and week_start and week_start.weekday() == 0:
                initial_data = {
                    "employee": selected_employee,
                    "week_start_date": week_start,
                }
                week_dates = [week_start + timedelta(days=offset) for offset in range(7)]
                work_date_ints = [_date_to_work_date_int(day) for day in week_dates]
                existing_entries = models.work_time.objects.filter(
                    employee_id=selected_employee.id,
                    work_date__in=work_date_ints,
                )

                rows_by_job = {}
                for entry in existing_entries:
                    job_key = entry.job_number_phase_cat_desc or ""
                    if job_key not in rows_by_job:
                        rows_by_job[job_key] = {day: 0 for day in day_fields}
                    day_index = work_date_ints.index(entry.work_date)
                    day_name = day_fields[day_index]
                    rows_by_job[job_key][day_name] += int(entry.hours_worked)

                initial_rows = []
                for job_item, hours_by_day in rows_by_job.items():
                    selected_job = job_phase_cat_desc.objects.filter(item=job_item).first()
                    if not selected_job:
                        continue

                    row_initial = {"job_number_phase_cat_desc": selected_job}
                    for day_name in day_fields:
                        row_initial[day_name] = hours_by_day[day_name]
                        daily_totals[day_name] += hours_by_day[day_name]
                    initial_rows.append(row_initial)

                row_formset = RowFormSet(initial=initial_rows or None, prefix="rows")

                mileage_entries = mileage_models.mileage_reimbursement.objects.filter(
                    employee=selected_employee,
                    mileage_date__range=(week_start, week_start + timedelta(days=6)),
                ).order_by("mileage_date")

                mileage_initial_rows = []
                for mileage_entry in mileage_entries:
                    mileage_initial_rows.append(
                        {
                            "mileage_date": mileage_entry.mileage_date,
                            "purpose": mileage_entry.purpose,
                            "miles": mileage_entry.miles,
                            "amount": mileage_entry.amount,
                            "job_number_phase_cat_desc": mileage_entry.job_number_phase_cat_desc,
                        }
                    )
                    mileage_total_miles += float(mileage_entry.miles)
                    mileage_total_amount += float(mileage_entry.amount)

                mileage_row_formset = MileageRowFormSet(initial=mileage_initial_rows or None, prefix="mileage_rows")

                auto_allowance_rows = mileage_models.auto_allowance_day.objects.filter(
                    allowance_date__range=(week_start, week_start + timedelta(days=6)),
                )
                allowance_by_date = {
                    entry.allowance_date: entry.mileage_reimbursement_allowed
                    for entry in auto_allowance_rows
                }
                for index, day_name in enumerate(day_fields):
                    auto_allowance[day_name] = allowance_by_date.get(week_dates[index], False)

                week_total = sum(daily_totals.values())
                form = forms.WeeklyTimecardForm(initial=initial_data)

    display_week_start = _display_week_start(form)
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_headers = [
        {"label": label, "date": _short_date(display_week_start + timedelta(days=index))}
        for index, label in enumerate(day_labels)
    ]

    return render(
        request,
        "app_work_hours/timecard.html",
        {
            "form": form,
            "row_formset": row_formset,
            "daily_totals": daily_totals,
            "week_total": week_total,
            "mileage_row_formset": mileage_row_formset,
            "mileage_total_miles": f"{mileage_total_miles:.2f}",
            "mileage_total_amount": f"{mileage_total_amount:.2f}",
            "auto_allowance": auto_allowance,
            "day_headers": day_headers,
            "employee_name": _display_employee_name(form),
            "period_ending": f"{(display_week_start + timedelta(days=6)).month}/{(display_week_start + timedelta(days=6)).day}/{(display_week_start + timedelta(days=6)).year}",
        },
    )


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
