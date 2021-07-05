
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from patients. models  import *
from django.contrib.auth import authenticate, login,logout
from .models import doctors,MedicalShop
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
import base64
from django.core.files.base import ContentFile
class index(TemplateView):
    template_name='admin/login.html'
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password =password)
        if user.is_superuser:
            login(request,user)
            return JsonResponse('true',safe=False)
        else:
            return render(request, 'admin/login.html')
class home(TemplateView):
    template_name='admin/index.html'
class DoctorsView(ListView):
    context_object_name = 'doctors'
    queryset = doctors.objects.all()

    template_name = 'admin/Doctorslist.html'
def AddDoctor(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            Name=request.POST['name']
            experience=request.POST['experience']
            email=request.POST['email']
            password1=request.POST['password1']
            password2=request.POST['password2']
            designation=request.POST['designation']
            department=request.POST['department']
            gender=request.POST['gender']
            number=request.POST['number']
            hospital=request.POST['hospital']
            address=request.POST['address']
            education=request.POST['education']
            image1=request.POST['image1']
            format ,imgstr = image1.split(';base64,')
            ext = format.split('/')[-1]
            img1=ContentFile(base64.b64decode(imgstr),name=Name+'.'+ext)
            if User.objects.filter(email=email).exists():
                return JsonResponse('false',safe=False)
            elif User.objects.filter(username=Name).exists():
                return JsonResponse('false1',safe=False)    
            elif doctors.objects.filter(mobile=number).exists():
                return JsonResponse('false2',safe=False)
            # elif (password1!=password2):
            #     return JsonResponse('false3',safe=False)

            if password1==password2:
                user = User.objects.create_user(username=Name, password=password1, email=email,first_name=Name)
                doctors.objects.create(experience=experience,designation=designation,doctor=user,
                department=department,gender=gender,mobile=number,hospital=hospital,address=address,profile_image=img1,education=education)
                send_mail(
        'Your login credential',
        'Username is your email and password is :'+str(password2),
        'favasm123@gmail.com',
        ['mailtofavazmuhammad@gmail.com'],
        fail_silently=False,
    )
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false3', safe=False)
        else:
            print("faaaaaaaaaaaaaa")
            return render(request,'admin/add_doctor.html')
    else:
        return redirect('index')
def add_shop(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name=request.POST['name']
            experience=request.POST['exp']
            email=request.POST['email']
            password=request.POST['password']
            place=request.POST['place']
            mobile=request.POST['mobile']
            if User.objects.filter(email=email).exists():
                return JsonResponse('false',safe=False)
            elif MedicalShop.objects.filter(mobile=mobile).exists():
                return JsonResponse('false1',safe=False)
            else:
                user = User.objects.create_user(username=name, password=password, email=email)
                MedicalShop.objects.create(experience=experience,place=place,mobile=mobile,shop=user)
                send_mail(
        'Your login credential',
        'Username is your email and password is :'+str(password),
        'favasm123@gmail.com',
        ['mailtofavazmuhammad@gmail.com'],
        fail_silently=False,
    )
                return JsonResponse('true',safe=False)

        else:
            
            return render(request,'admin/add_medicalshop.html')
    else:
        return redirect('index')
def doctor_block(request,id):
    if request.user.is_authenticated:
        user=User.objects.get(id=id)
        if user.is_active == True:
          user.is_active =False
          user.save()
          return redirect('doctors_list')
        else:
          user.is_active=True
          user.save()
          return redirect('doctors_list')
    else:
        return redirect('index')      
def doctor_delete(request,id):
    if request.user.is_authenticated:
        user= User.objects.get(id=id)
        user.delete()
        return redirect('doctors_list')
    else:
        return redirect('index')
class PatientsView(ListView):
    context_object_name = 'patients'
    queryset = patients.objects.all()
    template_name = 'admin/all_patients.html'
def patient_delete(request,id):
    if request.user.is_authenticated:
        user= User.objects.get(id=id)
        user.delete()
        return redirect('patients_list')
    else:
        return redirect('index')
def patient_block(request,id):
    if request.user.is_authenticated:
        user=User.objects.get(id=id)
        if user.is_active == True:
          user.is_active =False
          user.save()
          return redirect('patients_list')
        else:
          user.is_active=True
          user.save()
          return redirect('patients_list')
        
    else:
        return redirect('index')
def appointment(request):
    if request.user.is_authenticated:
       booking=Booking.objects.all()
       return render(request,'admin/appointments.html',{'booking':booking})
    else:
        return redirect('index')
def booking_cancel(request,id):
    if request.user.is_authenticated:
       booking=Booking.objects.get(id=id)
       booking.status='Cancel'
       booking.save()
       return redirect('appointments')
    else:
        return redirect('index')

def LogOut(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('index')
    else:
        return redirect('index')

