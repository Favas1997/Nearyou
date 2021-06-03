from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.index.as_view(),name='index'),
    path('home',views.home.as_view(),name='home'),
    path('patients_list',views.PatientsView.as_view(),name='patients_list'),
    path('add_doctor',views.AddDoctor.as_view(),name='add_doctor'),
    path('add_shop/',views.add_shop,name='add_shop')

]