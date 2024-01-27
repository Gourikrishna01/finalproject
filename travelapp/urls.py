from.views import *
from django.urls import path
from django.contrib.auth import views as auth_Views
app_name = 'travelapp'
urlpatterns = [

   path('',index,name='index'),
   path('login/',login,name='login'),
   path('register/',register,name='register'),
   path('home/',home,name='home'),
   path('logout/', logout, name='logout'),
   path('book/<str:pname>/',booking,name='book'),
   path('hotel/',HotelView,name='hotel'),
   path('book_hotel/<int:hotel_id>/',book_hotel,name='book_hotel'),
   path('carbook/<int:car_id>/', carbook, name='carbook'),
   path('carview/', Carlist, name='carview'),
   path('dashboard/',dashboard,name='dashboard'),
   path('package/',Package_list,name='package'),
   path('list/',hotel_list,name='list'),
   path('carlist/',car_list,name='carlist'),
   path('rating/<int:reservation_id>/',rating,name='rating')
  
 
  
]