from django.db import models
from django import forms
# Create your models here.
class doctors(models.Model):
    name=models.CharField(max_length=150)
    experience=models.IntegerField()
    designation = models.CharField(max_length=100)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    gender= models.CharField(max_length=50)
    hospital= models.CharField(max_length=100)
    address= models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    education= models.CharField(max_length=100)
    profile_image= models.ImageField(upload_to='media/')

    @property
    def imageurl(self):
        if self.profile_image == '':
            image = ''
        else:
            image = self.profile_image.url
        return image
