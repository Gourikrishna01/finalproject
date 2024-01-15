from.views import *
from django.urls import path
app_name = 'travelapp'
urlpatterns = [

   path('',index,name='index'),
   path('login/',login,name='login'),
   path('register/',register,name='register'),
   path('home/',home,name='home'),
   path('dashboard/',dashboard,name='dashboard'),
   path('logout/',logout,name='logout'),
   path('book/<str:pname>/',book,name='book'),
   path('hotel/',HotelView,name='hotel'),
   # path('password/',ResetPassword,name='password')
   path('book_hotel/<int:hotel_id>/',book_hotel,name='book_hotel')
 
]