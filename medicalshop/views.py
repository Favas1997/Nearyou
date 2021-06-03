from django.shortcuts import render,redirect
from Admin1.models import MedicalShop
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
# Create your views here.

def medical_login(request):
    if request.method=='POST':
        email=request.POST['email']
        
        password=request.POST['password']
        if MedicalShop.objects.filter(email=email).exists():
            
            return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:
        return render(request,'medicalshop/login.html')
def medical_home(request):
    return render(request,'medicalshop/index.html')