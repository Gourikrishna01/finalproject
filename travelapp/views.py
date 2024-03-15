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


def rating(request, reservation_id):
    if request.method == 'POST':
        reservation = Reservation.objects.get(id=reservation_id)
        user = request.user
        review_text = request.POST.get('review_text', '')

        # Check if the reservation belongs to the current user
        if reservation.user == user:
            Review.objects.create(package=reservation, user=user, review=review_text)
            messages.success(request, 'Review added successfully.')
            return redirect('travelapp:home')  # Redirect to the homepage after successful review
        else:
            messages.error(request, 'You are not authorized to review this package.')
            return redirect('travelapp:rating')  
    else:
        reservation = Reservation.objects.get(id=reservation_id)
        return render(request, 'Rating.html', {'reservation': reservation})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation
from django.contrib.auth.decorators import login_required

@login_required
def update_package(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    if request.method == 'POST':
        # Assuming you have form data in request.POST, you can directly update the model fields
        reservation.arrival_date = request.POST.get('arrival_date')
        reservation.departure_date = request.POST.get('departure_date')
        reservation.adult = request.POST.get('adult')
        reservation.children = request.POST.get('children')
        
        reservation.save()
        # Redirect to the package list view after update
        return redirect('travelapp:package')
    
    # Render a template with a form for updating the reservation
    return render(request, 'update_package.html', {'reservation': reservation})

   



def search(request):
    return render(request,'search.html')


def details(request):
    query=request.GET.get('query')
    package=Booking.objects.filter(pname__icontains=query)
    context={

        'package':package
    }
    return render(request,'details.html',context)

from django.shortcuts import render, get_object_or_404
from .models import Booking, Category, Places

def package_details(request, pname):
    package = get_object_or_404(Booking, pname=pname)
    categories = Category.objects.all()  # Retrieve all category objects
    category_id = request.GET.get('category_id')
    
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        # Retrieve places from the selected package and category
        places = Places.objects.filter(category_id=category_id, package=package)
    else:
        selected_category = None
        # Retrieve places from the selected package if no category is selected
        places = Places.objects.filter(package=package)
    
    context = {'categories': categories, 'places': places, 'selected_category': selected_category, 'package': package}
    return render(request, 'packages_details.html', context)




def popup_view(request, days_id):
    activities = Activities.objects.filter(days_id=days_id)
    return render(request, 'popup.html', {'activities': activities, 'days_id': days_id})



from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Itineary_user_details

def redirect_home(request):
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        activity = Activities.objects.get(id=activity_id)  # Assuming 'Activity' is your model for activities
        Itineary_user_details.objects.create(user=request.user, activity=activity.name)
        
        # Print a message to the terminal
        print(f"Activity '{activity.name}' added successfully by user '{request.user.username} and it is awiating for the approval of admin'.")

        return redirect('travelapp:home')

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
        # # and stored as datetime objects in the database
        # try:
        #     arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
        #     departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        # except ValueError:
        #     messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
        #     return redirect('booking_hotel', hotel_id=hotel_id)

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


from django.shortcuts import render, redirect
from .models import CarView, CarBook
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

@login_required
def carbook(request, car_id):
    if request.method == 'POST':
        arrival_date = request.POST.get('arrival_date')
        departure_date = request.POST.get('departure_date')
        destination = request.POST.get('destination')
        license_plate = request.POST.get('licesence')  # Corrected field name
        id_proof = request.POST.get('idproof')
      
        
        # Validate arrival and departure dates
        try:
            arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
            if departure_date <= arrival_date:
                raise ValueError("Departure date should be after arrival date.")
        except ValueError as e:
            messages.error(request, f"Error: {e}")
            return redirect('travelapp:carview', car_id=car_id)
        
        # Check car availability for the given dates
        car = CarView.objects.get(id=car_id)
        existing_bookings = CarBook.objects.filter(car_id=car, 
                                                    arrival_date__lte=departure_date, 
                                                    departure_date__gte=arrival_date)
        if existing_bookings.exists():
            messages.error(request, "Car is not available for the selected dates.")
            return redirect('travelapp:carview')
        
     
        # Create the booking
        user = request.user
        booking = CarBook.objects.create(user=user, car_id=car, arrival_date=arrival_date,
                                         departure_date=departure_date, destination=destination,
                                         licesence=license_plate, idproof=id_proof)
        booking.save()
        messages.success(request, "Car booked successfully!")
        return redirect('travelapp:carlist')
    else:
        # Handle GET request to show the form
        car = CarView.objects.get(id=car_id)
        return render(request, 'CarBooking.html', {'car': car})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from .models import userLogin

@login_required
def display_user_details(request):
    try:
        user_login = User.objects.get(username=request.user)
        return render(request, 'profile.html', {'user_login': user_login})
    except User.DoesNotExist:
        return HttpResponseNotFound("User details not found")
    except Exception as e:
        print(e)
        return HttpResponseNotFound("An error occurred")
from django.shortcuts import render, get_object_or_404
  # Correct the model name to Itinerary

def itinerary(request, package_id):
    package = get_object_or_404(Places, id=package_id)
    itineraries = Itineary.objects.filter(package=package)  # Correct the model name
    
    context = {'package': package, 'itineraries': itineraries}
    return render(request, 'itenary.html', context)  # Correct the template name to itinerary.html

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Reservation, Places

def book(request, package_id):
    if request.method == 'POST':
        # Assuming user is already logged in and stored in request.user
        user = request.user
        
        # Retrieve the package object
        package = Places.objects.get(id=package_id)
        
        # Assuming other data like date, adult, children are posted through the form
        arrival_date = request.POST.get('arrival_date')
        departure_date = request.POST.get('departure_date')
        adult = request.POST.get('adult')
        children = request.POST.get('children')
        
        # Check if a reservation already exists for the same package and date
        existing_reservation = Reservation.objects.filter(package=package, arrival_date=arrival_date).exists()
        
        if existing_reservation:
            # If a reservation already exists, display a message to the user
            messages.error(request, 'Sorry, this package is already booked for the selected date.')
            # Redirect back to the booking form
            return redirect(reverse('travelapp:book', kwargs={'package_id': package_id}))
        else:
            # Create Reservation object
            reservation = Reservation.objects.create(
                user=user, 
                package=package, 
                arrival_date=arrival_date, 
                departure_date=departure_date, 
                adult=adult, 
                children=children
            )
            
            # Redirect back to the home page after successful booking
            return redirect('travelapp:home')  # Assuming 'home' is the name of your home page URL pattern
    else:
        # Render the booking form template
        return render(request, 'Booking.html', {'package_id': package_id})


