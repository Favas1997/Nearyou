from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,ListView
from . models  import User,Booking
from . form import patientSignupForm 
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from Admin1.models import doctors
from doctors.models import Slot
import ast
from django.http import JsonResponse, HttpResponse
# Create your views here.
class Userindex(TemplateView):
    template_name = "patients/index.html"

class UserSignup(SuccessMessageMixin,CreateView):
    model = User
    form_class=patientSignupForm
    success_url = reverse_lazy('login')
    template_name="patients/signup.html"
    success_message = "Your profile was created successfully"

class Userlogin(View):
    def get(self,request):
        return render(request,'patients/login.html',{'form':AuthenticationForm})

    def post(self,request):
        form = AuthenticationForm(request, data=request.POST)
        print('haiiiiii')
        if form.is_valid():
            print("11111111111111")

            user = authenticate(request,username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
            if user is None:
                return render(request,'patients/login.html',{ 'form': form, 'invalid_creds': True })
            else:
                form.confirm_login_allowed(user)
                login(request, user)
                return redirect('Userindex')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('Userindex')
class DoctorView(ListView):
    context_object_name = 'doctors'
    queryset = doctors.objects.all()
    template_name='patients/doctors.html'
class Doctordetails(View):
    def get(self,request,id):
        details = doctors.objects.get(id=id)
        
        return render(request,'patients/doctor-details.html',{'doctor':details})
class booking(Doctordetails):
    def get(self,request,id):
        details = doctors.objects.get(id=id)
        slot=Slot.objects.get(doctor=id)
        slot.Slot_decided = ast.literal_eval(slot.Slot_decided)
        return render(request,'patients/appointment.html',{'doctor':details,'slots':slot})
    def post(self,request,id):
        date=request.POST.get('date')
        slot=request.POST.get('slot')
        Booking.objects.create(user=request.user,doctor_id=id,date=date,slot=slot,amount=200,status='confirm')
        return JsonResponse('true', safe=False)
class paymentView(TemplateView):
    template_name='patients/payment.html'

def time_slots(request, id):
    date = request.GET['date_selected']
    booking = Booking.objects.filter(date=date, doctor_id=id)
    used_slots = []
    for x in booking:
        used_slots.append(x.slot)
    return JsonResponse({'used_slots':used_slots})  

def profile(request):
    profile=User.objects.get(id=request.user.id)
    return render(request,'patients/profile.html',{'profile':profile})
def booking_details(request):
    details=Booking.objects.filter(user=request.user)
    return render(request,'patients/booking_list.html',{'booking':details})
def cancel(request,id):
    booking=Booking.objects.get(id=id)
    booking.status = "cancel"
    booking.save()
    return redirect (booking_details)
def delete(request,id):
    booking=Booking.objects.get(id=id)
    booking.delete()
    return redirect (booking_details)
