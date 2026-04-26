from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Athlete, Workout, WorkoutRecord


def home(request):
    athlete_count = Athlete.objects.count()
    workout_count = Workout.objects.count()
    record_count  = WorkoutRecord.objects.count()
    return render(request, 'core/home.html', {
        'athlete_count': athlete_count,
        'workout_count': workout_count,
        'record_count':  record_count,
    })


def workouts(request):
    if request.method == 'POST':
        action       = request.POST.get('action')
        workout_id   = request.POST.get('workout_id')
        workout_name = request.POST.get('workout_name', '').strip()
        workout_type = request.POST.get('workout_type', '').strip()
        errors = []
        if not workout_name:
            errors.append('Workout Name is required.')
        if not workout_type:
            errors.append('Workout Type is required.')
        if not errors:
            if action == 'add':
                Workout.objects.create(workout_name=workout_name, workout_type=workout_type)
                messages.success(request, 'Workout added successfully!')
                return redirect('workouts')
            elif action == 'edit' and workout_id:
                Workout.objects.filter(pk=workout_id).update(workout_name=workout_name, workout_type=workout_type)
                messages.success(request, 'Workout updated successfully!')
                return redirect('workouts')
            elif action == 'delete' and workout_id:
                Workout.objects.filter(pk=workout_id).delete()
                messages.success(request, 'Workout deleted.')
                return redirect('workouts')
        else:
            for e in errors:
                messages.error(request, e)
    all_workouts = Workout.objects.all()
    edit_id      = request.GET.get('edit')
    edit_workout = Workout.objects.filter(pk=edit_id).first() if edit_id else None
    return render(request, 'core/workouts.html', {
        'workouts':     all_workouts,
        'edit_workout': edit_workout,
    })


def records(request):
    if request.method == 'POST':
        action     = request.POST.get('action')
        athlete_id = request.POST.get('athlete_id')
        workout_id = request.POST.get('workout_id')
        duration   = request.POST.get('duration', '').strip()
        pace       = request.POST.get('pace', '').strip()
        avg_hr     = request.POST.get('avg_hr', '').strip()
        errors = []
        if not duration:
            errors.append('Duration is required.')
        if not pace:
            errors.append('Pace is required.')
        if not avg_hr:
            errors.append('Average Heart Rate is required.')
        else:
            try:
                hr = int(avg_hr)
                if hr <= 0 or hr > 300:
                    errors.append('Heart Rate must be between 1 and 300.')
            except ValueError:
                errors.append('Heart Rate must be a whole number.')
        if not errors:
            if action == 'add':
                try:
                    WorkoutRecord.objects.create(
                        athlete_id=athlete_id,
                        workout_id=workout_id,
                        duration=duration,
                        pace=pace,
                        average_hr=int(avg_hr)
                    )
                    messages.success(request, 'Workout logged successfully!')
                except Exception:
                    messages.error(request, 'A record for this athlete and workout already exists.')
                return redirect('records')
            elif action == 'edit':
                WorkoutRecord.objects.filter(
                    athlete_id=athlete_id, workout_id=workout_id
                ).update(duration=duration, pace=pace, average_hr=int(avg_hr))
                messages.success(request, 'Record updated successfully!')
                return redirect('records')
            elif action == 'delete':
                WorkoutRecord.objects.filter(
                    athlete_id=athlete_id, workout_id=workout_id
                ).delete()
                messages.success(request, 'Record deleted.')
                return redirect('records')
        else:
            for e in errors:
                messages.error(request, e)
    all_records   = WorkoutRecord.objects.select_related('athlete', 'workout').order_by(
        'workout__workout_type', 'athlete__athlete_name'
    )
    athletes      = Athlete.objects.all()
    workout_types = Workout.objects.values_list('workout_type', flat=True).distinct()
    edit_key      = request.GET.get('edit')
    edit_record   = None
    if edit_key:
        try:
            aid, wid    = edit_key.split('_')
            edit_record = WorkoutRecord.objects.get(athlete_id=aid, workout_id=wid)
        except Exception:
            pass
    filter_type = request.GET.get('type', 'All')
    if filter_type != 'All':
        all_records = all_records.filter(workout__workout_type=filter_type)
    return render(request, 'core/records.html', {
        'records':       all_records,
        'athletes':      athletes,
        'workout_types': workout_types,
        'filter_type':   filter_type,
        'edit_record':   edit_record,
        'workouts':      Workout.objects.all(),
    })