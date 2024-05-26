from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # Use username parameter for email
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("index")  # Redirect to the home page or another appropriate page
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserLoginForm()
    
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")  # Redirect to the login page
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def contact(request):
    return render(request, "contact.html")

def products(request):
    return render(request, "products.html")

def services(request):
    return render(request, "services.html")

def item_view(request):
    return render(request, 'item.html')

def cart_view(request):
    return render(request, 'cart.html')

def about(request):
    return render(request, 'about.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if not email:
            messages.error(request, 'Email is required')
            return render(request, 'forgot-password.html')
        user = User.objects.filter(email=email)
        if user.exists():
            print(user)
            user = User.objects.get(email=email)
            return redirect('reset-password')
        else:
            messages.error(request, "Email not found")
            return render(request, 'forgot-password.html')

    return render(request, 'forgot-password.html')

def reset_password(request):
    return render(request, 'password-reset.html')

def logout_view(request):
    logout(request)
    return redirect('index')