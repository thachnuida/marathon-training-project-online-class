from django.db import models
from django.conf import settings
from home.models import *
from django.contrib.auth.models import User

# Create your models here.
class Class(models.Model):
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User)
    students_in_class = models.ManyToManyField(User, related_name="students_in_class", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    image_class = models.ImageField(upload_to="class_management", null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.class_name

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100)
    Class = models.ForeignKey(Class)
    description = models.TextField(null=True, blank=True)
    video_link = models.URLField(max_length=45)
    create_date = models.DateTimeField(auto_now_add=True)
    latest_update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.lesson_name


class Test(models.Model):
    lesson = models.ForeignKey(Lesson)
    test_name = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    latest_update_date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.test_name


class Question(models.Model):
    question = models.CharField(max_length=255)
    answerA = models.CharField(max_length=255)
    answerB = models.CharField(max_length=255)
    answerC = models.CharField(max_length=255)
    answerD = models.CharField(max_length=255)
    image_ques = models.ImageField(upload_to="test", null=True, blank=True) 
    right_answer = models.CharField(max_length=1)
    test = models.ForeignKey(Test)
    order_test = models.IntegerField()
    
    def __unicode__(self):
        return self.question
