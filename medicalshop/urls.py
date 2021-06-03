from django.urls import path

from . import views

urlpatterns = [
    
    path('/',views.medical_login,name="medical_login"),
    path('/medical_home/',views.medical_home,name='medical_home')

]  