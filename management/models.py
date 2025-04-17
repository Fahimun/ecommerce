from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
        ROLE_CHOICES = [
            ('Admin', 'Admin'),
            ('Staff', 'Staff'),
            ('Customer', 'Customer '),
        ]
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        team_id = models.IntegerField(blank=True, null=True)
        last_seen = models.DateTimeField(blank=True,null=True)
        role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CREATED')
        bio = models.TextField(max_length=500, blank=True)
        location = models.CharField(max_length=30, blank=True)
        birth_date = models.DateField(null=True, blank=True)
        image = models.FileField(upload_to='image/',blank=True,null=True)
        profile_image = models.ImageField(upload_to='profile/image/')
        phone_number = models.CharField(blank=True,null=True,max_length=11)
        email_verification_code = models.CharField(max_length=6, blank=True, null=True)
        forgot_password_token = models.CharField(max_length=200, blank=True, null=True)
        is_email_active = models.BooleanField(default=False)
      


  
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    age = models.IntegerField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Name: { self.name}  //  Age: {self.age}"
    

class Category(models.Model):
     product_tittle=models.CharField(max_length=100)
     product_description=models.TextField()
     created_at=models.DateTimeField(auto_created=True)

     def __str__(self):
        return f"Name: {self.product_tittle}  //  description: {self.product_description}" 
     
class Tag(models.Model):
    name = models.CharField(max_length=500, unique=True) 

    def __str__(self):
        return self.name    
    
class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_info = models.TextField(blank=True, null=True) 

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    product_image = models.ImageField(upload_to='product_image/')
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f"Name: { self.product_name}  //  description: {self.description}" 
    

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"    
