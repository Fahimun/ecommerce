from django.db import models
from django.contrib.auth.models import User
from management.models import *
from django.utils.crypto import get_random_string
from django.utils import timezone
import uuid

 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the item was added

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in {self.user.username}'s cart"
    


