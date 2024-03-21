from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class SavedEvents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    image = models.CharField(max_length=128)
    date = models.CharField(max_length=32, blank=True)
    time = models.CharField(max_length=16, blank=True)
    venue = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    link = models.CharField(max_length=128)
    favorite = models.BooleanField()
