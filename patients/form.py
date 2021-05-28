from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from patients. models import User
class patientSignupForm(UserCreationForm):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    phone_number=forms.CharField(required=True)
    place=forms.CharField(required=True)
    age=forms.IntegerField(required=True)
    gender=forms.CharField(required=True)
    blood_group=forms.CharField(required=True)
    class Meta:
        model=User
        fields = ['username','email', 'first_name','last_name','phone_number','place','age','gender','blood_group']
        
    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is not unique')
        return email
    def clean_phone_number(self):
        phone_number=self.cleaned_data.get("phone_number")
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Number is not unique')
        return phone_number

        
