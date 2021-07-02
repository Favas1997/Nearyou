from django.db import models

# Create your models here.
from Admin1.models import MedicalShop
from patients.models import Booking

class descriptions(models.Model):
    description=models.CharField(max_length=300)
    medicalshop=models.ForeignKey(MedicalShop,on_delete=models.CASCADE)
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    code=models.TextField(blank=True, null=True)