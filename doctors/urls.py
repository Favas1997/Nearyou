from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.index,name='index-doctor'),
    path('home/',views.home,name='home-doctor'),
    path('password_change/<int:id>/',views.change_password,name='password_change'),
    path('addschedule/<int:id>/',views.addschedule,name="addschedule"),
    path('view_appointment/<int:id>/',views.view_appoinment,name="view_appointment"),
    path('Logout/',views.Logout,name='Logout')
    

]  