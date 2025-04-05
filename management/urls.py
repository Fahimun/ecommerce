from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),

    path('profile/',profile,name='profile'),
    path('add_product/',add_product,name='add_product'),
    path('products/',products,name='products'),
    path('contacts/',contacts,name='contacts'),
    path('add_contact/',add_contact,name='add_contact'),
    path('edit_product/<int:id>/',edit_product,name='edit_product'),
    path('delete_product/<int:id>/',delete_product,name='delete_product'),
    path('product_view/',product_view,name='product_view'),
]

