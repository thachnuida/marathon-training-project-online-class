from django.db import models

# Create your models here.
class Role(models.Model):
    role = models.CharField(max_length=255)
    def __unicode__(self):
        return self.role

class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=32)
    fullname = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    role = models.ForeignKey(Role)
    user_image = models.ImageField(upload_to="images/users/", help_text="50x180px")
    gender = models.CharField(max_length=10)
    def __unicode__(self):
        return self.username
