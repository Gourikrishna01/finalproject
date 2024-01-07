from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userLogin(models.Model):
        username = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
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
       user=models.ForeignKey(userLogin,on_delete=models.CASCADE,related_name='user_reservations')
       package=models.ForeignKey(Booking,on_delete=models.CASCADE)
       checkIN=models.DateField(null=True,blank=True)
       checkOut=models.DateField(null=True,blank=True)
       adult=models.IntegerField(null=True,blank=True)
       Children=models.IntegerField(null=True,blank=True)
#        email=models.ForeignKey(userLogin,on_delete=models.CASCADE,related_name='email_reservations')
       def _str_(self):
        return f"Booking for {self.user} at {self.package}"
      

class Hotel(models.Model):
    
      name=models.CharField(max_length=100)
      address=models.TextField(max_length=100)
      image=models.ImageField(upload_to='travelimages/',blank=True)
      price=models.IntegerField()
      def __str__(self) :
            return str(self.name)



       