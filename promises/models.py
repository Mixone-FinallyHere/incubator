from django.db import models

# Create your models here.

class Promise(models.Model):
    
    start = models.DateTimeField()
    stop = models.DateTimeField()
    user = models.ForeignKey('users.User')
    is_sure = models.BooleanField(default=True)


class Slot(models.Model):

    start = models.DateTimeField()
    stop = models.DateTimeField()
    is_weekly_recurrent = models.BooleanField(default=False)
