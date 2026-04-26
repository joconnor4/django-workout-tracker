from django.contrib import admin
from .models import Athlete

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display  = ('athlete_name', 'phone', 'birth_date', 'grad_year')
    search_fields = ('athlete_name', 'phone')
    list_filter   = ('grad_year',)
    ordering      = ('athlete_name',)