from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userLogin(models.Model):
        username = models.TextField(User,unique=True)
        fullname=models.CharField(max_length=20)
        email=models.CharField(max_length=20)
        password=models.CharField(max_length=20)
        
        def __str__(self):
                return str(self.user.username)


class Booking(models.Model):
    pname=models.CharField(max_length=20,primary_key=True)
    amount=models.IntegerField()
    images=models.ImageField(upload_to='travelimages/',blank=True)

    def __str__(self) :
           return str(self.pname)
    


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Booking, on_delete=models.CASCADE)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    adult = models.IntegerField(null=True, blank=True)
    children = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
         
        return f"Booking for {self.user} at {self.package}"
       

class Hotel(models.Model):
    
      name=models.CharField(max_length=100)
      address=models.TextField(max_length=100)
      images=models.ImageField(upload_to='travelimages/',blank=True)
      price=models.IntegerField()
      def __str__(self) :
            return str(self.name)


class HotelConfirm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=255)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    adult_count = models.IntegerField()
    children_count = models.IntegerField()
    def _str_(self):
        return f"Booking for {self.user} at {self.hotel_id}"


class CarView(models.Model):
      brand=models.CharField(max_length=100)
      model=models.CharField(max_length=100)
      year=models.IntegerField()
      seats=models.IntegerField()
      image=models.ImageField(upload_to='travelimages/',blank=True)
      def __str__(self):
            return str(self.brand)
      




class CarBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_id = models.ForeignKey(CarView, on_delete=models.CASCADE)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    destination = models.CharField(max_length=50)

    def __str__(self):
        return f"Booking for {self.user} at {self.car_id}"

class Review(models.Model):
     package = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='ratings')
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     review=models.CharField(max_length=300)

     def __str__(self):
        return f"Booking for {self.user} at {self.package}"