from django.urls import path,include

from .import views

urlpatterns = [
    
    path('',views.Userindex.as_view(),name='Userindex'),
    path('signup/',views.UserSignup.as_view(),name='signup'),
    path('login/',views.Userlogin.as_view(),name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('doctorslist/',views.DoctorView.as_view(),name='doctorslist'),
    path('doctor-details/<int:id>/',views.Doctordetails.as_view(),name='doctor-details'),
    path('appointment/<int:id>/',views.booking.as_view(),name='appointment'),
    path('payment/',views.paymentView.as_view(),name='paymentView'),
    path('time-slots/<int:id>/',views.time_slots,name='time-slots'),
    path('profile/',views.profile,name='profile'),
    path('booking_list/',views.booking_details,name='booking_list'),
    path('cancel/<int:id>/',views.cancel,name='cancel'),
    path('Delete/<int:id>/',views.delete,name='Delete')


]  