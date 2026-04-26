from django.urls import path
from . import views

urlpatterns = [
    path('',          views.home,     name='home'),
    path('workouts/', views.workouts, name='workouts'),
    path('records/',  views.records,  name='records'),
]