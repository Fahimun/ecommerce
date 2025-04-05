from django.urls import path
from .views import *



urlpatterns = [
    path('',dasboard,name='dasboard'),
    path('signin/',signin,name='signin'),
    path('signup/',signup,name='signup'),
    path('logout_view/',logout_view,name='logout_view'),
    path("card_list/",card_list, name="card_list"), 
    path("add_to_cart/<int:product_id>/",add_to_cart, name="add_to_cart"), 
    
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', reset_password , name='reset_password'),
    path("reset/done/", pass_reset_complete, name="pass_reset_complete"),
    path('reset/<uidb64>/<token>/',pass_reset_confirm , name='pass_reset_confirm'),
    path('change_password/', change_password, name='change_password'),



    path('send_email/', send_email, name='send_email'),
  

]

