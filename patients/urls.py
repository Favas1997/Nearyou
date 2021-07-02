from django.urls import path,include

from .import views

urlpatterns = [
    
    path('',views.Userindex,name='Userindex'),
    path('signup/',views.Signup,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('doctorslist/',views.DoctorView.as_view(),name='doctorslist'),
    path('doctor-details/<int:id>/',views.Doctordetails.as_view(),name='doctor-details'),
    path('appointment/<int:id>/',views.booking,name='appointment'),
    path('payment/',views.paymentView.as_view(),name='paymentView'),
    path('time-slots/<int:id>/',views.time_slots,name='time-slots'),
    path('profile/',views.profile,name='profile'),
    path('booking_list/',views.booking_details,name='booking_list'),
    path('cancel/<int:id>/',views.cancel,name='cancel'),
    path('Delete/<int:id>/',views.delete,name='Delete'),
    path('videoCall/<str:roomCode>/',views.videoCall,name='videoCall'),
    path('description/',views.description,name='description'),
    path('addimage/',views.addimage,name='addimage')


]  