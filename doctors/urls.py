from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.index.as_view(),name='index-doctor'),
    path('home/',views.home,name='home-doctor'),
    path('change_password/<int:id>/',views.change_password,name='change_password'),
    path('addschedule/<int:id>/',views.addschedule,name="addschedule"),
    path('view_appointment/<int:id>/',views.view_appoinment,name="view_appointment")
    

]  