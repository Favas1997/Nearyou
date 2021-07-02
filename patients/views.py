from django.shortcuts import render,redirect
from django.views.generic import ListView,TemplateView
from medicalshop.models import descriptions
from . models import *
import random
import uuid
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views import View
from Admin1.models import doctors,MedicalShop
from doctors.models import Slot
import ast
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from datetime import date


# Create your views here.
def Userindex(request): 
    print(type(1))
    return render(request,'patients/index.html')
def Signup(request):
    if request.user.is_authenticated:
        return redirect('Userindex')
    else:
        if request.method=='POST':
            username = request.POST['username']
            name=request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            place=request.POST['place']
            Age=request.POST['age']
            blood=request.POST['blood_group']
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif patients.objects.filter(phone_number=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                user = User.objects.create_user(username=username, password=password, email=email,first_name=name)
                patients.objects.create(user=user, phone_number=phone,place=place,age=Age,blood_group=blood)

                return JsonResponse('true', safe=False)
            
        else:
            return render(request,'patients/signup.html')
def Login(request):
    if request.user.is_authenticated:
        return redirect('Userindex')
    else:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if patients.objects.filter(user_id=user.id):
                    auth.login(request, user)
                    user.is_staff=True
                    user.save()
                    return JsonResponse('true', safe=False)
                else:
                    return JsonResponse('false',safe=False) 
            else:
                return JsonResponse('false',safe=False)
            
        else:

            return render(request,'patients/login.html')
class DoctorView(ListView):
    context_object_name = 'doctors'
    queryset = doctors.objects.all()
    template_name='patients/doctors.html'
    
class Doctordetails(View):
    def get(self,request,id):
        details = doctors.objects.get(id=id)
        return render(request,'patients/doctor-details.html',{'doctor':details})
def booking(request,id):
    if request.user.is_authenticated:
        details = doctors.objects.get(id=id)
        slot=Slot.objects.get(doctor=id)
        slot.Slot_decided = ast.literal_eval(slot.Slot_decided)
        if request.method=='POST':
            date=request.POST.get('date')
            slot=request.POST.get('slot')
            check=slot.split("-")
            print(check)
            code = uuid.uuid4().hex
            patient=patients.objects.get(user_id=request.user.id)
            Room=chatroom.objects.create(roomcode=code,user=patient,doctor_id=id)
            Booking.objects.create(user=patient,doctor_id=id,date=date,slot=slot,amount=200,status='confirm',Room=Room)
            return JsonResponse('true', safe=False)
        else:
            return render(request,'patients/appointment.html',{'doctor':details,'slots':slot})
    else:
        return redirect('login')

# class booking(Doctordetails):
#     def get(self,request,id):
#         details = doctors.objects.get(id=id)
#         slot=Slot.objects.get(doctor=id)
#         slot.Slot_decided = ast.literal_eval(slot.Slot_decided)
#         return render(request,'patients/appointment.html',{'doctor':details,'slots':slot})
#     def post(self,request,id):
#         date=request.POST.get('date')
#         slot=request.POST.get('slot')
#         check=slot.split("-")
#         print(check)
#         code = uuid.uuid4().hex
#         patient=patients.objects.get(user_id=request.user.id)
#         Room=chatroom.objects.create(roomcode=code,user=patient,doctor_id=id)
#         Booking.objects.create(user=patient,doctor_id=id,date=date,slot=slot,amount=200,status='confirm',Room=Room)
        
#         return JsonResponse('true', safe=False)
class paymentView(TemplateView):
    template_name='patients/payment.html'

def time_slots(request, id):
    if request.user.is_authenticated:
        date = request.GET['date_selected']
        booking = Booking.objects.filter(date=date, doctor_id=id)
        used_slots = []
        for x in booking:
            used_slots.append(x.slot)
        return JsonResponse({'used_slots':used_slots})  
    else:
        return redirect('login')
def profile(request):
    if request.user.is_authenticated:
        profile=patients.objects.get(user_id=request.user.id)
        return render(request,'patients/profile.html',{'profile':profile})
    else:
        return redirect('login')
def booking_details(request):
    if request.user.is_authenticated:
        y= date.today()
        patient=patients.objects.get(user_id=request.user.id)
        details=Booking.objects.filter(user=patient)
        return render(request,'patients/booking_list.html',{'booking':details,'today':y})
    else:
        return redirect('login')
def cancel(request,id):
    if request.user.is_authenticated:
        booking=Booking.objects.get(id=id)
        booking.status = "cancel"
        booking.save()
        return redirect (booking_details)
    else:
        return redirect('login')
def delete(request,id):
    if request.user.is_authenticated:
        booking=Booking.objects.get(id=id)
        booking.delete()
        return redirect (booking_details)
    else:
        return redirect('login')
def videoCall(request,roomCode):
    if request.user.is_authenticated:
        room = chatroom.objects.get(roomcode=roomCode)
        request.session['code']=roomCode
        if room.user.user==request.user or room.doctor.doctor==request.user:
            if patients.objects.filter(user_id=request.user.id).exists():
                target=patients.objects.get(user_id=request.user.id)
                status=User.objects.get(id=room.doctor.doctor.id)
                print(status.is_staff)
                context = {'roomCode': roomCode, 'target': target,'status':status}
            else:
                target=doctors.objects.get(doctor_id=request.user.id)
                doctor=User.objects.get(id=room.user.user.id)
                print(doctor.is_staff)
                shop=MedicalShop.objects.all()
                check=target.doctor_id
                context = {'roomCode': roomCode, 'target': target,'check':check,'shop':shop,'doctor':doctor}
            return render(request, 'patients/video.html', context)
        return redirect('login')
    else:
        return redirect('login')
def logout(request):
    if request.user.is_authenticated:
        user=request.user
        user.is_staff=False
        user.save()
        auth.logout(request)
        
        return redirect('Userindex')
    else:
        return redirect('Userindex')
def description(request):
    if request.user.is_authenticated:
        description=request.POST['description']

        code=request.session['code']
        securitycode=random.randint(1000,9999)
        
        med=MedicalShop.objects.get(id=3)
        booking=Booking.objects.get(Room=chatroom.objects.get(roomcode=code))
        descriptions.objects.create(description=description,medicalshop=med,booking=booking,code=securitycode)
        send_mail(
        'Your login credential',
        'Username is your email and password is :'+str(securitycode),
        'favasm123@gmail.com',
        ['mailtofavazmuhammad@gmail.com'],
        fail_silently=False,
    )

        return JsonResponse('true', safe=False)
    else:
        return redirect('login')
        
def addimage(request):
    if request.user.is_authenticated:
        image=request.FILES.get('image_upload')
        user=patients.objects.get(user=request.user)
        user.image=image
        user.save()
        return JsonResponse('true',safe=False)
    else:
        return redirect('login')

