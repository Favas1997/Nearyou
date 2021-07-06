from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from Admin1.models import MedicalShop, doctors
from django.http import JsonResponse, HttpResponse
import random
from django.core import serializers
from django.contrib.auth.models import User,auth
from twilio.rest import Client
from . models import *
from patients.models import patients
# Create your views here.

def medical_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(username=username, password =password)
        if user is not None:
            if MedicalShop.objects.filter(shop_id=request.user.id).exists():
                auth.login(request, user)
                return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:
        return render(request,'medicalshop/login.html')
def medical_home(request):
    return render(request,'medicalshop/index.html')
def otplogin(request):
    if request.method=='POST':
        mobile=request.POST['mobile']
        if MedicalShop.objects.filter(mobile=mobile).exists():
            request.session['mobile']=mobile
            random_num=random.randint(1000,9999)
            global Otp
            Otp=random_num
                   
            account_sid='ACd8b6d36444c43589f82b8499ce1c78fb'
            auth_token='dba409c19b5b4ef07ac7677fd57d1ba9'
            client=Client(account_sid,auth_token)

            message=client.messages.create(
                         body=f"your otp for login is {Otp}",
                         from_='+18057197626',
                         to=f'+916282680439'
                    )
                    
            return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:
        return render(request,'medicalshop/otplogin.html')
def otpcheck(request):
    if request.method =='POST':
        mobile=request.session['mobile']
        shop=MedicalShop.objects.get(mobile=mobile)
        user1=User.objects.get(id=shop.shop_id)
        otp_entered = request.POST['otp']
          
        global Otp
        if Otp == int(otp_entered) :
            auth.login(request,user1,backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse('true',safe=False)

    else:
        return render(request,'medicalshop/otpcheck.html')
def description(request):
    if request.method=='POST':
        print('favaaa')
        security=request.POST['security']
        if descriptions.objects.filter(code=security).exists():
            request.session['description']=security
            return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:

        return render(request,'medicalshop/search.html')
def getdescription(request):
    security=request.session['description']
    prescription=descriptions.objects.get(code=security)
    return render(request,'medicalshop/prescription.html',{'prescription':prescription})