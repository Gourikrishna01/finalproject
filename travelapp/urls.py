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
  
   path('hotel/',HotelView,name='hotel'),
   path('book_hotel/<int:hotel_id>/',book_hotel,name='book_hotel'),
   path('carbook/<int:car_id>/', carbook, name='carbook'),
   path('carview/', Carlist, name='carview'),
   path('dashboard/',dashboard,name='dashboard'),
   path('package/',Package_list,name='package'),
   path('list/',hotel_list,name='list'),
   path('carlist/',car_list,name='carlist'),
   path('rating/<int:reservation_id>//update/',rating,name='rating'),

   path('update/<int:reservation_id>/', update_package, name='update'),
   path('search/',search,name='search'),
   path('details/',details,name='details'),
   path('package-details/<str:pname>/', package_details, name='package_details'),
   path('itinerary/<int:package_id>/', itinerary, name='itinerary'),  # Your existing itinerary URL pattern
   path('popup/<int:days_id>/', popup_view, name='popup'), 
   
   path('redirect_home/' , redirect_home, name='redirect_home'),
   path('profile/', display_user_details, name='profile'),
  path('book/<int:package_id>/', book, name='book')
]
   
  


  
 
  
