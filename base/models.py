from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

from shop import settings
    
class Product(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilogram'),
        ('l', 'Liter'),
    ]

    CATEGORY_CHOICES = [
        ('cat1', 'Category 1'),
        ('cat2', 'Category 2'),
        ('cat3', 'Category 3'),
    ]

    name = models.CharField(max_length=100, null=False, blank=False)    
    description = models.CharField(max_length=700, null=False, blank=False)
    price = models.FloatField(validators=[MinValueValidator(0.1)], blank=False, null=False)
    amount = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    unit = models.CharField(choices=UNIT_CHOICES, max_length=3)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"
    
class Contact(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=100, null=False)
    phone_number = models.CharField(max_length=20, null=False)
    email = models.EmailField(null= False)
    image = models.ImageField(upload_to='workers_images/', default='F:\shop\media\workers_images\default.jpg')

class Coupon(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=100, null=False)
    number = models.CharField(max_length=20, null=False)
    active = models.BooleanField(default=True, verbose_name='Active')

class New(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='news_images/')

    def __str__(self):
        return self.title
    
    def short_description(self):
        return self.description[:30] + '... read in details'
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    answer_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_new = models.BooleanField(default=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    PICKUP_LOCATIONS = [
        ('Location 1', 'Location 1'),
        ('Location 2', 'Location 2'),
        ('Location 3', 'Location 3'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    pickup_location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0.0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}" 
    
class  Partner(models.Model):
    logo_image = models.ImageField(upload_to="partners_logo/")
    partner_url = models.URLField()
    partner_name = models.TextField(default="partner")

class AboutUs(models.Model):
    name = models.CharField(max_length=255, default="Welcome to About Us Section")  
    information = models.TextField()           
    video = models.FileField(upload_to='videos/', default='F:\Уник\СТРВЕБ\MWD\static\videos\y2meta.com - EPIC INTRO NO TEXT(360p).mp4')   
    logo = models.ImageField(upload_to='logos/', blank=True)
    history = models.TextField(blank=True)     
    details = models.TextField(blank=True)     
    certificate = models.ImageField() 

    def __str__(self):
        return self.name