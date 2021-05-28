from django.shortcuts import render,redirect

# Create your views here.

def medical_login(request):

    return render(request,'medicalshop/login.html')