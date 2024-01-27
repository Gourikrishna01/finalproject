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
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation, Booking

def booking(request, pname):
    if request.method == 'POST':
        booking = Booking.objects.get(pname=pname)
        user = request.user
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        adult = request.POST.get('adult')
        children = request.POST.get('children')
        
        # Check if there's any existing reservation for the same date
        existing_reservation = Reservation.objects.filter(package=booking, check_in=check_in).exists()
        
        if existing_reservation:
            # Alert message for already booked date
            messages.error(request, f"This package is already booked for {check_in}. Please choose a different date.")
            return redirect('travelapp:book', pname=pname)
        else:
            # Create a new Reservation instance
            reservation = Reservation(user=user, package=booking, check_in=check_in, check_out=check_out, adult=adult, children=children)
            reservation.save()
            # Redirect to a success page or home page
            return redirect('travelapp:home')
    else:
        # Render the booking form
        return render(request, 'Booking.html', {'pname': pname})

def HotelView(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'HotelView.html', context)



def book_hotel(request, hotel_id):
    hotel_instance = get_object_or_404(Hotel, pk=hotel_id)

    if request.method == 'POST':
        room_type = request.POST.get('room_type')
        arrival_date = request.POST.get('arrival_date')
        departure_date = request.POST.get('departure_date')
        adult_count = request.POST.get('adult_count')
        children_count = request.POST.get('children_count')

        user_instance = request.user

        # Ensure that dates are parsed correctly (assuming proper format from the form)
        # and stored as datetime objects in the database
        try:
            arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
            return redirect('booking_hotel', hotel_id=hotel_id)

        # Check for existing bookings on the selected dates
        existing_booking = HotelConfirm.objects.filter(
            hotel=hotel_instance,
            arrival_date=arrival_date,
            departure_date=departure_date,
        )

        if existing_booking.exists():
            # If a booking already exists, display an error message
            messages.error(request, 'This hotel is already booked for the selected dates.')
            return redirect('travelapp:hotel')
            

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
            messages.success(request, 'Hotel booking successful!')
            return redirect('travelapp:home')  # Redirect to home page after successful booking

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



def dashboard(request):
   return render(request, 'dashboard.html')


def Package_list(request):
   
    # Retrieve all reservations made by the current user
    user_reservations = Reservation.objects.filter(user=request.user)
    context = {'user_reservations': user_reservations}
    return render(request, 'Packages_list.html', context)
   

def hotel_list(request):
    # Retrieve hotel bookings for the current user
    user_bookings = HotelConfirm.objects.filter(user=request.user)
    
    # Pass the bookings to the template for rendering
    return render(request, 'hotel_list.html', {'user_bookings': user_bookings})


from django.shortcuts import render
from .models import CarBook  # Assuming you have a CarBook model defined

def car_list(request):
    # Filter car bookings for the current user
    car_bookings = CarBook.objects.filter(user=request.user)
    context = {'car_bookings': car_bookings}
    return render(request, 'Car_list.html', context)


from django.shortcuts import render, redirect
from .models import Review, Reservation
from django.contrib.auth.decorators import login_required

@login_required
def rating(request, reservation_id):
    if request.method == 'POST':
        reservation = Reservation.objects.get(id=reservation_id)
        user = request.user
        review_text = request.POST.get('review_text', '')

        # Check if the reservation belongs to the current user
        if reservation.user == user:
            Review.objects.create(package=reservation, user=user, review=review_text)
            return redirect('travelapp:home')  # Redirect to the homepage after successful review
        else:
            return render(request, 'error.html', {'error_message': 'You are not authorized to review this package.'})
    else:
        reservation = Reservation.objects.get(id=reservation_id)
        return render(request, 'Rating.html', {'reservation': reservation})
