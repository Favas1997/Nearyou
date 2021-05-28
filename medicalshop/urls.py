from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.medical_login,name="medical_login"),

]  