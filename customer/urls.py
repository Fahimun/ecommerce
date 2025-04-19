from django.urls import path
from .views import *



urlpatterns = [
    path('',dasboard,name='dasboard'),
    path('signin/',signin,name='signin'),
    path('signup/',signup,name='signup'),
    path('logout_view/',logout_view,name='logout_view'),
    path("card_list/",card_list, name="card_list"), 
    path("add_to_cart/<int:product_id>/",add_to_cart, name="add_to_cart"), 
    
    path('forget_password/', forget_password, name='forget_password'),
    path('change_password/<str:token>/', change_password, name='change_password'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),

    path('send_email/', send_email, name='send_email'),
    path('verify_email/', verify_email, name='verify_email'),
  

]

