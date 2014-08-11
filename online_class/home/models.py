from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    TEACHER= 'T'
    STUDENT= 'F'
    ROLE_CHOICES = (
    (TEACHER, 'Teacher'),
    (STUDENT, 'Student'),
    )
    MALE = 'M'
    FEMALE = 'F'
    GENDERS_CHOICES = ((MALE, 'Male'),
               (FEMALE, 'Female'))

    # slug = models.SlugField(max_length=10,blank=True)
    birthday = models.DateField(blank=True,null=True)
    address = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=12,blank=True)
    role= models.CharField(max_length=2,choices=ROLE_CHOICES)
    gender =models.CharField(max_length=2,choices=GENDERS_CHOICES)
    user_image = models.ImageField(upload_to="home", null=True, blank=True)

    def __unicode__(self):
        return self.user.username
# class Teacher(User):
#     def __unicode__(self):
#         return self.username

# # class Student(User):
#     def __unicode__(self):
#         return self.username
