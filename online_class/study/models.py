from django.db import models
from django.conf import settings
from home.models import *
from django.contrib.auth.models import User
from class_management.models import *
# Create your models here.
class Score(models.Model):
    score = models.IntegerField(max_length=20)
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    test_date = models.DateTimeField(auto_now_add=True)

