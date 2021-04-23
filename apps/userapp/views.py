from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404

from apps.product.models import Product
from .models import CustomUser
from apps.vendor.models import Vendor

from .forms import RegisterForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
    
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            role = data['role']

            user = User()
            user.username = username
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            customUser = CustomUser()
            customUser.user = user
            customUser.role =role
            customUser.contact = phone
            customUser.address = address
            customUser.zipcode = zipcode
        
            #generate otp
            #customUser.otp = otp
            #sendsms(otp)
            customUser.save()

            if role=='VEN':
                vendor = Vendor.objects.create(name='default', created_by=user)
                vendor.save()

            login(request, user)

            if role=='VEN':
                return redirect('vendor_admin')
            
            if role=='CUS':
                return redirect('frontpage')

            return redirect('frontpage')
    else:
        form = RegisterForm()

    return render(request, 'userapp/signup.html', {'form': form})