from django.contrib.auth.models import User
from django.db import models


# Model inherited from TicketMaster project
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Model made by William
class SavedNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    image = models.CharField(max_length=128)
    date = models.CharField(max_length=32, blank=True)
    time = models.CharField(max_length=16, blank=True)
    content = models.CharField(max_length=256, blank=True)
    favorite = models.BooleanField()


# Model made by William
class PrivatePublicKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    privateKey1 = models.IntegerField()
    privateKey2 = models.IntegerField()
    publicKey1 = models.IntegerField()
    publicKey2 = models.IntegerField()
