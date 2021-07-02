from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache 
import datetime
from consulting import settings
# Create your models here.
class doctors(models.Model):
    doctor= models.OneToOneField(User, on_delete=models.CASCADE)
    experience=models.IntegerField()
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    gender= models.CharField(max_length=50)
    hospital= models.CharField(max_length=100)
    address= models.CharField(max_length=100)
    mobile = models.CharField(max_length=20,unique=True)
    education= models.CharField(max_length=100)
    profile_image= models.ImageField(upload_to='media/')

    @property
    def imageurl(self):
        if self.profile_image == '':
            image = ''
        else:
            image = self.profile_image.url
        return image
    def last_seen(self):
        return cache.get('seen_%s' % self.doctor.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False  
class MedicalShop(models.Model):
    shop=models.OneToOneField(User, on_delete=models.CASCADE)
    experience=models.IntegerField()
    mobile = models.CharField(max_length=20,unique=True)
    place = models.CharField(max_length=20)