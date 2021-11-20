from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    name = models.CharField(max_length=30)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Meeting(models.Model):
    name = models.CharField(max_length=30)
    ##minutes
    length = models.IntegerField()
    #priority = models.PositiveBigIntegerField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.name