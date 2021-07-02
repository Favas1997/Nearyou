from patients.models import patients
from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.index.as_view(),name='index'),
    path('home',views.home.as_view(),name='home'),
    path('doctors_list',views.DoctorsView.as_view(),name='doctors_list'),
    path('add_doctor/',views.AddDoctor,name='add_doctor'),
    path('add_shop/',views.add_shop,name='add_shop'),
    path('Doctor_block/<int:id>/',views.doctor_block,name='Doctor_block'),
    path('Doctor_delete/<int:id>/',views.doctor_delete,name='Doctor_delete'),
    path('patients_list/',views.PatientsView.as_view(),name='patients_list'),
    path('patient_block/<int:id>/',views.patient_block,name='patient_block'),
    path('patient_delete/<int:id>/',views.patient_delete,name='patient_delete'),
    path('appointments/',views.appointment,name='appointments'),
    path('booking_cancel/<int:id>/',views.booking_cancel,name='booking_cancel'),
    path('LogOut/',views.LogOut,name='LogOut')




]