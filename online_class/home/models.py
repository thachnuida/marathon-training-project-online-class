from django.db import models

class User(models.Model):
    username = models.CharField(max_length=10)
    slug = models.SlugField(max_length=10)
    password = models.CharField(max_length=32)
    fullname = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    

class Teacher(User):
    def __unicode__(self):
        return self.username

class Student(User):
    def __unicode__(self):
        return self.username
