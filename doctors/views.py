
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from Admin1.models import doctors
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages
from . models import Slot
from patients.models import Booking
from datetime import date

# Create your views here.
class index(TemplateView):
    template_name='doctors/login.html'
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        doctor=doctors.objects.get(email=username)
        if doctor is not None:
            request.session['key'] = doctor.id
            return redirect('home-doctor')
            
            return redirect('index-doctor')
def home(request):
    key=request.session['key']
    context=doctors.objects.get(id=key)
    booking=Booking.objects.filter(doctor=key,date=date.today())
    print(date)
    return render(request,'doctors/index.html',{'doctor':context,'booking':booking})
def change_password(request,id):
    doctor=doctors.objects.get(id=id)
    if request.method == 'POST':
        current_entered=request.POST['current_password']    
        current_password=doctor.password
        new_password=request.POST['password']
        check = check_password(current_entered,current_password)
        if check == True:
            doctor.password=make_password(new_password)
            doctor.save()
            return redirect('home-doctor')
        else:
            messages.info('password does not much')
        
    else:
        return render(request,'doctors/password.html',{'doctor':doctor})
def addschedule(request,id):
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
def view_appoinment(request,id):
    booked=Booking.objects.filter(doctor_id=id)
    doctor=doctors.objects.get(id=id)
    return render(request,'doctors/view_appointment.html',{'booked':booked,'doctor':doctor})
