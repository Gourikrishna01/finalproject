from.views import *
from django.urls import path
from django.contrib.auth import views as auth_Views
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
   path('password/',password,name='password'),
   path('book_hotel/<int:hotel_id>/',book_hotel,name='book_hotel'),
   path('carbook/<int:car_id>/', carbook, name='carbook'),
   path('carview/', Carlist, name='carview'),
   path('search/',search,name='search'),
   path('details/',details,name='details'),
    path('rate-package/<int:package_id>/', Rating, name='rate-package'),
  
]