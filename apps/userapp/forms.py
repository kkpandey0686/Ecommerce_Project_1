from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    userChoice = (
        ('VEN', 'vendor'),
        ('CUS', 'customer'),
        ('WHO', 'wholeseller'),
        ('DEL', 'delivery'),
        ('OTH', 'other'),
    )

    role = forms.ChoiceField(choices=userChoice, required=False)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)


    # class Meta:
    #     model = User
    #     fields = ("username", "password", "role", )