from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

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