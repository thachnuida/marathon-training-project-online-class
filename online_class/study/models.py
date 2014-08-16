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
    def get_max_score(user, test):
    	return Score.objects.filter(test=test, user=user).aggregate(Max('score'))['score__max']

