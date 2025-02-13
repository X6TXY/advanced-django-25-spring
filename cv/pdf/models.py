from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    summary = models.TextField(max_length=1500)
    degree = models.CharField(max_length=250)
    school = models.CharField(max_length=250)
    university = models.CharField(max_length=250)
    previous_work = models.TextField(max_length=1500)
    skills = models.TextField(max_length=1500)
    employed = models.BooleanField(default=False)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()


class CV(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)