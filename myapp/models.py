from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from .choices import CATEGORIES
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, phone_number, first_name=None, last_name=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of birth, phone number,first name, last name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, phone_number=phone_number,first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, phone_number,first_name=None, last_name=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of birth, phone number, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, date_of_birth, phone_number, first_name, last_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    objects = CustomUserManager()

    REQUIRED_FIELDS = ["date_of_birth", "phone_number", "first_name", "last_name"]
    USERNAME_FIELD = "email"


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    def is_valid(self):
        # Define the expiration duration (e.g., 10 minutes)
        expiration_duration = timezone.timedelta(minutes=10)
        # Calculate the expiration timestamp
        expiration_timestamp = self.created_at + expiration_duration
        # Check if the current time is before the expiration timestamp
        return timezone.now() < expiration_timestamp
    
class Category(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Drug(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='drugs')
    image = models.ImageField(upload_to='drug_images/')
    best_sellers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()  # Add this line to include tags

    def __str__(self):
        return self.title



# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     drugs = models.ManyToManyField(Drug, through='OrderItem')
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()