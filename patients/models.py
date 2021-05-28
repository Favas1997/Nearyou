from django.contrib.auth.models import AbstractUser
from django.db import models
from Admin1.models import doctors
# Create your models here.
class User(AbstractUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email = models.EmailField(max_length=70,blank=True)
    phone_number=models.CharField(max_length=20)
    place=models.CharField(max_length=100)
    age=models.IntegerField(null=True)
    gender=models.CharField(null=True,max_length=8)
    blood_group=models.CharField(null=True,max_length=4)

class Booking(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    doctor=models.ForeignKey(doctors,on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.CharField(max_length=20, null=True, blank=True)
    amount=models.CharField(max_length=10)
    status=models.CharField(max_length=20,default='Pending')