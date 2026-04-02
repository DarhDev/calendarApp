from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import calendar as std_calendar
from .models import Event, Reminder, Appointment
from .forms import EventForm, ReminderForm, AppointmentForm
from django.contrib import messages
from collections import defaultdict


@login_required(login_url='admin:login')
def calendar_view(request):
    """Main calendar view for the year 2026"""
    year = int(request.GET.get('year', 2026))
    month = int(request.GET.get('month', timezone.now().month))

    
    # Get calendar for the month
    cal = std_calendar.monthcalendar(year, month)
    
    # Get events for the month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    events = Event.objects.filter(
        user=request.user,
        start_date__gte=start_date,
        start_date__lt=end_date
    )
    
    # Get appointments for the month
    appointments = Appointment.objects.filter(
        user=request.user,
        start_time__gte=start_date,
        start_time__lt=end_date
    )
    
    # Get upcoming reminders
    reminders = Reminder.objects.filter(
        event__user=request.user,
        is_sent=False,
        reminder_time__lt=timezone.now() + timedelta(days=7)
    ).select_related('event')
    
    # Organize events and appointments by day
    events_by_day = defaultdict(list)
    appointments_by_day = defaultdict(list)
    
    for event in events:
        day = event.start_date.day
        events_by_day[day].append(event)

    
    for appointment in appointments:
        day = appointment.start_time.day
        appointments_by_day[day].append(appointment)
    
    # Determine available dates (dates without events or appointments)
    available_dates = set()
    for week in cal:
        for day in week:
            if day > 0 and day not in events_by_day and day not in appointments_by_day:
                available_dates.add(day)

    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    context = {
        'year': year,
        'month': month,
        'month_name': std_calendar.month_name[month],
        'calendar': cal,
        'events': events,
        'appointments': appointments,
        'reminders': reminders,
        'events_by_day': events_by_day,
        'appointments_by_day': appointments_by_day,
        'available_dates': available_dates,
        'today': timezone.now().date(),
        'daynames': day_names,
    }
    return render(request, 'events/calendar.html', context)


@login_required(login_url='admin:login')
def event_list(request):
    """View to list all events"""
    events = Event.objects.filter(user=request.user).order_by('start_date')
    context = {'events': events}
    return render(request, 'events/event_list.html', context)


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def create_event(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.full_clean()
            event.save()
            print("Event created successfully!")
            messages.info(request, "Event created successfully!")
            return redirect('events:event_detail', pk=event.pk)
        else:
            print("Form errors:", form.errors)  
            messages.error(request, "Please correct the errors below.")   
    form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required(login_url='admin:login')
def event_detail(request, pk):
    """View event details"""
    event = get_object_or_404(Event, pk=pk, user=request.user)
    reminders = event.reminders.all()
    context = {'event': event, 'reminders': reminders}
    return render(request, 'events/event_detail.html', context)


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def edit_event(request, pk):
    """Edit an existing event"""
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.full_clean()
            event.save()
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'event': event, 'title': 'Edit Event'})


@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def delete_event(request, pk):
    """Delete an event"""
    event = get_object_or_404(Event, pk=pk, user=request.user)
    event.delete()
    return redirect('events:event_list')


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def create_reminder(request, event_pk):
    """Create a reminder for an event"""
    event = get_object_or_404(Event, pk=event_pk, user=request.user)
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.event = event
            reminder.save()
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = ReminderForm()
    return render(request, 'events/reminder_form.html', {'form': form, 'event': event})


@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def delete_reminder(request, pk):
    """Delete a reminder"""
    reminder = get_object_or_404(Reminder, pk=pk, event__user=request.user)
    event_pk = reminder.event.pk
    reminder.delete()
    return redirect('events:event_detail', pk=event_pk)


@login_required(login_url='admin:login')
def appointment_list(request):
    """View to list all appointments"""
    appointments = Appointment.objects.filter(user=request.user).order_by('start_time')
    context = {'appointments': appointments}
    return render(request, 'events/appointment_list.html', context)


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def create_appointment(request):
    """Create a new appointment"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.full_clean()
            appointment.save()
            return redirect('events:appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    return render(request, 'events/appointment_form.html', {'form': form, 'title': 'Create Appointment'})


@login_required(login_url='admin:login')
def appointment_detail(request, pk):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    context = {'appointment': appointment}
    return render(request, 'events/appointment_detail.html', context)


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def edit_appointment(request, pk):
    print(f"Editing appointment with pk={pk}")  # Debugging statement
    """Edit an existing appointment"""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.full_clean()
            appointment.save()
            return redirect('events:appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'events/appointment_form.html', {'form': form, 'appointment': appointment, 'title': 'Edit Appointment'})


@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def delete_appointment(request, pk):
    """Delete an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    appointment.delete()
    return redirect('events:appointment_list')


@login_required(login_url='admin:login')
def dashboard(request):
    today = timezone.now()
    next_7_days = today + timedelta(days=7)
    
    upcoming_events = Event.objects.filter(
        user=request.user,
        start_date__gte=today,
        start_date__lt=next_7_days
    ).order_by('start_date')
    
    
    upcoming_appointments = Appointment.objects.filter(
        user=request.user,
        start_time__gte=today,
        start_time__lt=next_7_days
    ).order_by('start_time')
    print("Upcoming Appointment:", upcoming_appointments.count())  # Debugging statement
    print(Appointment.objects.all())  # Debugging statement to check all events in the database
    
    context = {
        'upcoming_events': upcoming_events,
        'upcoming_appointments': upcoming_appointments,
        'events_count': upcoming_events.count(),
        'appointments_count': upcoming_appointments.count(),
        'today': today,
    }
    
    return render(request, 'events/dashboard.html', context)



