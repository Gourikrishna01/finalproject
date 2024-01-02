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
    




       

      



       