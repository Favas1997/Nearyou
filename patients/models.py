from django.contrib.auth.models import User
from django.db import models
from Admin1.models import doctors
from django.core.cache import cache 
import datetime
from consulting import settings

# Create your models here.
class patients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=20,unique=True)
    place=models.CharField(max_length=100)
    age=models.IntegerField(null=True)
    gender=models.CharField(null=True,max_length=8)
    blood_group=models.CharField(null=True,max_length=4)
    image= models.ImageField(upload_to='media/')
    @property
    def imageurl1(self):
        if self.image == '':
            image = ''
        else:
            image = self.image.url
        return image
class chatroom(models.Model):
    roomcode = models.TextField(blank=True, null=True)
    user= models.ForeignKey(patients, on_delete=models.SET_NULL, blank=True, null=True)
    doctor= models.ForeignKey(doctors, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.roomcode


class Booking(models.Model):
    user =models.ForeignKey(patients,on_delete=models.CASCADE)
    Room =models.ForeignKey(chatroom,on_delete=models.CASCADE,null=True)
    doctor=models.ForeignKey(doctors,on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.CharField(max_length=20, null=True, blank=True)
    amount=models.CharField(max_length=10)
    status=models.CharField(max_length=20,default='Pending')
    

