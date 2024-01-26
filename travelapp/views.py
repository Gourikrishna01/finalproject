# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.views import LogoutView

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


from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Booking, Reservation

@login_required
def book(request, pname):
    try:
        # Get the package instance
        package_instance = Booking.objects.get(pname=pname)
    except Booking.DoesNotExist:
        raise Http404("Package does not exist")

    packagename = package_instance.pname

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        adult_count = request.POST.get('adult_count')
        children_count = request.POST.get('children_count')

        # Get the current logged-in user
        user_instance = request.user  # Use request.user directly

        # Check for existing reservation
        existing_reservation = Reservation.objects.filter(
            user=user_instance,
            package=package_instance,
            checkIN=check_in_date,
        )

        if existing_reservation.exists():
            messages.error(request, 'This package is already booked for the selected date.')
        else:
            try:
                # Create a new reservation
                reservation = Reservation.objects.create(
                    user=user_instance,
                    package=package_instance,
                    checkIN=check_in_date,
                    checkOut=check_out_date,
                    adult=adult_count,
                    children=children_count,
                )
                reservation.save()

                messages.success(request, 'Booking successful!')
                return redirect('home')  # Redirect to home page after successful booking

            except Exception as e:
                messages.error(request, 'An error occurred while booking. Please try again.')

    return render(request, 'Booking.html', {'packagename': packagename})




def HotelView(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'HotelView.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Hotel, HotelConfirm

def book_hotel(request, hotel_id):
    hotel_instance = get_object_or_404(Hotel, pk=hotel_id)

    if request.method == 'POST':
        room_type = request.POST.get('room_type')
        arrival_date = request.POST.get('arrival_date')
        departure_date = request.POST.get('departure_date')
        adult_count = request.POST.get('adult_count')
        children_count = request.POST.get('children_count')

        user_instance = request.user

        # Check for existing bookings on the selected dates
        existing_booking = HotelConfirm.objects.filter(
            user=user_instance,
            hotel=hotel_instance,
            arrival_date=arrival_date,
            departure_date=departure_date,
        )

        if existing_booking.exists():
            # If a booking already exists, display an error message
            messages.error(request, 'This hotel is already booked for the selected dates.')
            return render(request, 'Booking_hotel.html', {'hotel_instance': hotel_instance, 'hotel_id': hotel_id})

        if room_type:
            # Use the fetched hotel_instance when creating HotelConfirm
            booking = HotelConfirm.objects.create(
                user=user_instance,
                hotel=hotel_instance,
                room_type=room_type,
                arrival_date=arrival_date,
                departure_date=departure_date,
                adult_count=adult_count,
                children_count=children_count
            )
            booking.save()

            messages.success(request, 'Hotel booking successful!')
            return redirect('travelapp:home')

    return render(request, 'Booking_hotel.html', {'hotel_instance': hotel_instance, 'hotel_id': hotel_id})



# views.py
def Carlist(request):
    cars=CarView.objects.all()
    context={'cars':cars}
    return render(request,'CarView.html',context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import CarView, CarBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def carbook(request, car_id):
    car_instance = get_object_or_404(CarView, pk=car_id)

    if request.method == 'POST':
        arrival_date = request.POST.get('arrival_date')
        departure_date = request.POST.get('departure_date')
        destination = request.POST.get('destination')

        user_instance = request.user if isinstance(request.user, User) else None

        if user_instance and arrival_date and departure_date and destination:
            # Check for existing bookings on the selected dates
            existing_booking = CarBook.objects.filter(
                user=user_instance,
                car_id=car_instance,
                arrival_date=arrival_date,
                departure_date=departure_date,
            )

            if existing_booking.exists():
                # If a booking already exists, display an error message
                print(f"User {user_instance.username} attempted to book car {car_instance} on the same dates again.")

                messages.error(request, 'This car is already booked for the selected dates.')
                return render(request, 'CarBooking.html', {'car_instance': car_instance, 'car_id': car_id})

            # If no existing booking, create a new one
            booking = CarBook.objects.create(
                user=user_instance,
                car_id=car_instance,
                arrival_date=arrival_date,
                departure_date=departure_date,
                destination=destination
            )
            booking.save()

            messages.success(request, 'Car booking successful!')
            return redirect('travelapp:home')
        else:
            messages.error(request, 'Some fields are missing')

    return render(request, 'CarBooking.html', {'car_instance': car_instance, 'car_id': car_id})

# views.py

def search(request):
    return render(request,'search.html')


def details(request):
    query=request.GET.get('query')
    package=Booking.objects.filter(pname__icontains=query)
    context={

        'package':package
    }
    return render(request,'details.html',context)




def password(request):
    return render(request,'Forget.html')
from django.shortcuts import render, redirect
from .models import Review

def rating(request, package_id):
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        package = Booking.objects.get(pk=package_id)
        review = Review(package=package, user=request.user, review=review_text)
        review.save()
        return redirect('home')  # Redirect to home page after successful review
    else:
        # Handle GET request if needed
        return render(request,'Rating.html')
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reservation
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Filter reservations based on the current logged-in user
        user_reservations = Reservation.objects.filter(user=request.user.id)
        # Pass the user's reservations to the template
        return render(request, 'dashboard.html', {'user_reservations': user_reservations})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('login')
