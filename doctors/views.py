from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from Admin1.models import doctors
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages
from . models import Slot
from patients.models import Booking 
from datetime import date
from django.contrib.auth.models import User, auth

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home-doctor')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if doctors.objects.filter(doctor=user).exists():
                doctor=doctors.objects.get(doctor=user)
                if doctor is not None:
                    auth.login(request, user)
                    user.is_staff=True
                    user.save()

                    request.session['key'] = doctor.id
                    return JsonResponse('true',safe=False)
            else:  
                return JsonResponse('false',safe=False)
        else:
            return render(request,'doctors/login.html')
def home(request):
    if request.user.is_authenticated:
        try:
            key=request.session['key']
        except:
            return redirect('index-doctor')    
        host=request.get_host()
        context=doctors.objects.get(id=key)
        booking=Booking.objects.filter(doctor=key,date=date.today())
        booking_list=Booking.objects.filter(doctor=key)
        return render(request,'doctors/index.html',{'doctor':context,'booking':booking,'host':host,'list':booking_list})
    else:
       return redirect('index-doctor') 
def change_password(request,id):
    if request.user.is_authenticated:
        user=User.objects.get(id=id)
        if request.method == 'POST':
            current_entered=request.POST['current_password']    
            current_password=request.user.password
            new_password=request.POST['password']
            check = check_password(current_entered,current_password)
            if check == True:
                user.set_password(new_password)
                user.save()
                return redirect('home-doctor')
            else:
                messages.info('password does not much')   
        else:
            doctor=doctors.objects.get(doctor_id=id)
        return render(request,'doctors/password.html',{'doctor':doctor,'user':user})
    else:
        return redirect('index-doctor')
def addschedule(request,id):
    if request.user.is_authenticated:
        doctor=doctors.objects.get(id=id)
        if request.method=='POST':
            am1 = request.POST.getlist('10AM-10.30AM')
            am2 = request.POST.getlist('10.30AM-11.00AM')
            am3 = request.POST.getlist('11.00AM-11.30AM')
            am4 = request.POST.getlist('11.30AM-12.00PM')
            am5 = request.POST.getlist('12.00PM-12.30PM')
            pm1= request.POST.getlist('4.00PM-4.30PM')
            pm2= request.POST.getlist('4.30PM-5.00PM')
            pm3= request.POST.getlist('5.00PM-5.30PM')
            pm4= request.POST.getlist('5.30PM-6.00PM')
            slot=am1+am2+am3+am4+am5+pm1+pm2+pm3+pm4
            if Slot.objects.filter(doctor=doctor).exists():
                previous_slot=Slot.objects.filter(doctor=doctor)
                previous_slot.delete()
            Slot.objects.create(doctor=doctor,Slot_decided=slot)
            return redirect(home)
        else:
            return render(request,'doctors/schedule.html',{'doctor':doctor})
    else:
        return redirect('index-doctor')
def view_appoinment(request,id):
    if request.user.is_authenticated:
        booked=Booking.objects.filter(doctor_id=id)
        doctor=doctors.objects.get(id=id)
        return render(request,'doctors/view_appoint.html',{'booked':booked,'doctor':doctor})
    else:
        return redirect('index-doctor')
def Logout(request):
    if request.user.is_authenticated:
        user=request.user
        user.is_staff=False
        user.save()
        auth.logout(request)
        
        return redirect('index-doctor')
    else:
        return redirect('index-doctor')
