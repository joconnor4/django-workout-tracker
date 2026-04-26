from django.db import models

class Athlete(models.Model):
    athleteid    = models.AutoField(primary_key=True, db_column='athleteid')
    athlete_name = models.CharField(max_length=30, db_column='athletename')
    phone        = models.CharField(max_length=10, db_column='phone')
    birth_date   = models.DateField(db_column='birthdate')
    grad_year    = models.CharField(max_length=4, db_column='gradyear')

    class Meta:
        db_table = 'athletes'
        ordering = ['athlete_name']

    def __str__(self):
        return self.athlete_name


class Workout(models.Model):
    workoutid    = models.AutoField(primary_key=True, db_column='workoutid')
    workout_name = models.CharField(max_length=20, db_column='workoutname')
    workout_type = models.CharField(max_length=20, db_column='workouttype')

    class Meta:
        db_table = 'workouts'
        ordering = ['workout_type', 'workout_name']

    def __str__(self):
        return f"{self.workout_name} ({self.workout_type})"


class WorkoutRecord(models.Model):
    athlete      = models.ForeignKey(Athlete, on_delete=models.CASCADE, db_column='athleteid', primary_key=True)
    workout      = models.ForeignKey(Workout, on_delete=models.CASCADE, db_column='workoutid')
    duration     = models.CharField(max_length=20, null=True, blank=True, db_column='duration')
    pace         = models.CharField(max_length=20, null=True, blank=True, db_column='pace')
    average_hr   = models.IntegerField(null=True, blank=True, db_column='averagehr')

    class Meta:
        db_table = 'workoutrecords'
        unique_together = ('athlete', 'workout')

    def __str__(self):
        return f"{self.athlete} — {self.workout}"