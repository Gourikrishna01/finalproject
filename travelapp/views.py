# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from datetime import datetime
def index(request):
     packages = Booking.objects.all()
     context={'packages':packages}
     return render(request,'index.html',context)




def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        email = request.POST['email']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('travelapp:register')  # Redirect to the registration page

        myuser = User.objects.create_user(username=username, password=password, email=email)
        myuser.fullname = fullname
        myuser.save()

        messages.success(request, "Account created successfully")
        return redirect('travelapp:login')

    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            fname = user.get_full_name() if user.get_full_name() else user.username
            return redirect('travelapp:home')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('travelapp:login')

    return render(request, 'login.html')


def home(request):
    packages=Booking.objects.all()
    context={'packages':packages}
    return render(request,'home.html',context)

def dashboard(request):
    return render(request,'dashboard.html')



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


def Book(request,pname):
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        checkin=request.POST['checkin']
        checkout=request.POST['checkout']
        duration_of_stay=request.POST['duration_of_stay']
        duration_of_choice=request.POST['duration_of_choice']
        adult=request.POST['adult']
        children=request.POST['children']

        if username and email and checkin and checkout and duration_of_choice and duration_of_stay:
            package = Booking.objects.get(pk=pname)

            booking = Booking.objects.create(
                user_name=username,
                email=email,
                package=package,
                check_in=checkin,
                check_out=checkout,
                adult=adult,
                children=children,
                duration_of_stay=duration_of_stay,
                duration_of_choice=duration_of_choice

            )

            booking.save()

            # Redirect to a success page or any other desired page
            return redirect('booking_success')

    # If the request method is not POST or there are validation errors, render the booking form
    package = Booking.objects.get(pk=pname)
    return render(request, 'book_package.html', {'package': package})
