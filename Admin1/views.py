
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from patients. models  import User
from django.contrib.auth import authenticate, login,logout
from .models import doctors,MedicalShop
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
class index(TemplateView):
    template_name='admin/login.html'
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password =password)
        if user.is_superuser:
            login(request,user)
            return redirect('home')
        else:
            return render(request, 'admin/login.html')
class home(TemplateView):
    template_name='admin/index.html'
class PatientsView(ListView):
    context_object_name = 'patients'
    queryset = User.objects.all()
    template_name = 'admin/all_patients.html'
class AddDoctor(TemplateView):
    template_name='admin/add_doctor.html'
    def post(self,request):
        name=request.POST.get('name')
        experience=request.POST.get('experience')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        designation=request.POST.get('designation')
        department=request.POST.get('department')
        gender=request.POST.get('gender')
        number=request.POST.get('number')
        hospital=request.POST.get('hospital')
        address=request.POST.get('address')
        image=request.FILES.get('profile')
        education=request.POST.get('education')
        if password1==password2:
            password1=make_password(password1)
            doctors.objects.create(name=name,experience=experience,email=email,password=password1,designation=designation,
            department=department,gender=gender,mobile=number,hospital=hospital,address=address,profile_image=image,education=education)
            send_mail(
    'Your login credential',
    'Username is your email and password is :'+str(password2),
    'favasm123@gmail.com',
    ['mailtofavazmuhammad@gmail.com'],
    fail_silently=False,
)
            return render(request,'admin/index.html')
def add_shop(request):
    if request.method == 'POST':
        name=request.POST['name']
        experience=request.POST['exp']
        email=request.POST['email']
        password=request.POST['password']
        place=request.POST['place']
        mobile=request.POST['mobile']
        if MedicalShop.objects.filter(email=email).exists():
            return JsonResponse('false',safe=False)
        elif MedicalShop.objects.filter(mobile=mobile).exists():
            return JsonResponse('false1',safe=False)
        else:
            MedicalShop.objects.create(name=name,experience=experience,email=email,password=make_password(password),place=place,mobile=mobile)
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

        

