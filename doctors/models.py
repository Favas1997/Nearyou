from django.db import models
from Admin1.models import doctors
# Create your models here.
class Slot(models.Model):
    doctor =models.ForeignKey(doctors,on_delete=models.CASCADE)
    Slot_decided=models.TextField( null=True, blank=True)
