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


class Category(models.Model):
     Categoryname=models.CharField(max_length=200)
     def __str__(self):
          return str(self.Categoryname)


class Booking(models.Model):
    pname=models.CharField(max_length=20,primary_key=True)
    amount=models.IntegerField()
    images=models.ImageField(upload_to='travelimages/',blank=True)
    description=models.CharField(max_length=100)

    


    def __str__(self) :
           return str(self.pname)
    


       

class Hotel(models.Model):
    
      name=models.CharField(max_length=100)
      address=models.TextField(max_length=100)
      images=models.ImageField(upload_to='travelimages/',blank=True)
      price=models.IntegerField()
      roomtype=models.CharField(max_length=100)
      checkout=models.IntegerField()
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
      petrolcharge=models.IntegerField()
      rent=models.IntegerField()
      def __str__(self):
            return str(self.brand)
      




class CarBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_id = models.ForeignKey(CarView, on_delete=models.CASCADE)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    destination = models.CharField(max_length=50)
    licesence=models.CharField(max_length=100)
    idproof=models.IntegerField()
    deposit=models.IntegerField()

    def __str__(self):
        return f"Booking for {self.user} at {self.car_id}"







class Places(models.Model):
     category=models.ForeignKey(Category,on_delete=models.CASCADE)
     name=models.CharField(max_length=200)
     days=models.IntegerField()
     night=models.IntegerField()
     image=models.ImageField(upload_to='travelimages/',blank=True)
     description=models.CharField(max_length=2000)
 
     

     def __str__(self):
          return f"{self.name}  - {self.category}" 
     


class Itineary(models.Model):
    place=models.ForeignKey(Places,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    name=models.CharField(max_length=50)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    date = models.DateField()
    month = models.CharField(max_length=50)
    day_of_week = models.CharField(max_length=50)

    def display_format(self):
        # Format the date as "DD Mon, Day"
        return f"{self.date.strftime('%d %b')}, {self.day_of_week}"
    
    def  __str__(self):
         return f"{self.name} - {self.display_format()}"


    
    

class Activities(models.Model):
     name=models.CharField(max_length=100)
     details=models.CharField(max_length=200)
     image=models.ImageField(upload_to='travelimages/')
     price=models.IntegerField()

     def  __str__(self):
          return self.name
     
class Itenary_User_Details(models.Model):
     itenary=models.ForeignKey(Itineary,on_delete=models.CASCADE)
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     activity=models.ForeignKey(Activities,on_delete=models.CASCADE)



class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Places, on_delete=models.CASCADE)
    date=models.DateField()
    adult = models.IntegerField(null=True, blank=True)
    children = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
         
        return f"Booking for {self.user} at {self.package}"
    


class Review(models.Model):
     package = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='ratings')
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     review=models.CharField(max_length=300)

     def __str__(self):
        return f"Booking for {self.user} at {self.package}"