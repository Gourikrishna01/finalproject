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
            # request.session[user.id] = id
            fname = user.get_full_name() if user.get_full_name() else user.username
            return redirect('travelapp:home')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('travelapp:login')

    return render(request, 'login.html')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


def home(request):
    packages=Booking.objects.all()
    context={'packages':packages}
    
    return render(request,'home.html',context)
    

def dashboard(request):
    return render(request,'dashboard.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import userLogin
from .models import Booking, Reservation

@login_required
def book(request, pname):
    # Initialize packagename with a default value
    packagename = None

    if request.method == 'POST':
        # Assuming you get the user and package instances based on package_id
        user_instance = request.user  # Assuming user is authenticated

        # Check if userLogin instance exists, create it if not
        user_login_instance, created = userLogin.objects.get_or_create(username=user_instance)

        package_instance = Booking.objects.get(pname=pname)
        packagename = package_instance.pname

        # Extract other form data from POST request
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        adult_count = request.POST.get('adult_count')
        children_count = request.POST.get('children_count')

        # Get the email from the userLogin instance
       

        # Create a reservation instance
        reservation = Reservation(
            user=user_login_instance,
            package=package_instance,
            checkIN=check_in_date,
            checkOut=check_out_date,
            adult=adult_count,
            Children=children_count,
          
        )

        # Save the reservation
        reservation.save()

        # Display a success message
        messages.success(request, 'Booking successful!')

        # Redirect to the home page
        return redirect('travelapp:home')

    # If the request is not POST, render the booking form
    return render(request, 'Booking.html', {'pname': pname, 'packagename': packagename})


def HotelView(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'HotelView.html', context)



# def ResetPassword(request):
#     return render(request,'Forget.html')