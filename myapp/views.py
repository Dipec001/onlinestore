from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import User, OneTimePassword, Drug, Category, Cart, CartItem
from .utils import send_otp_for_password_reset
from django.contrib.auth.decorators import user_passes_test
from .permissions import admin_check
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
import os
import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create your views here.
def index(request):
    categories = Category.objects.all()
    best_sellers = Drug.objects.filter(best_sellers__gt=0)  # Filter drugs with best_sellers > 0
    return render(request, 'index.html', {'categories':categories, 'best_sellers': best_sellers})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # Use username parameter for email
            if user is not None:
                login(request, user)

                # Merge session cart items with the authenticated user's cart
                if 'cart_id' in request.session:
                    session_cart_id = request.session['cart_id']
                    try:
                        session_cart = Cart.objects.get(id=session_cart_id)
                        user_cart, created = Cart.objects.get_or_create(user=user)

                        # Transfer items from session cart to user cart
                        for session_cart_item in session_cart.cartitem_set.all():
                            user_cart_item, created = CartItem.objects.get_or_create(
                                cart=user_cart, drug=session_cart_item.drug)
                            if not created:
                                user_cart_item.quantity += session_cart_item.quantity
                            else:
                                user_cart_item.quantity = session_cart_item.quantity
                            user_cart_item.save()

                        # Clear the session cart
                        session_cart.delete()
                        del request.session['cart_id']
                    except Cart.DoesNotExist:
                        pass
                
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


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        if not email:
            messages.error(request, 'Email is required')
            return render(request, 'forgot-password.html')
        user = User.objects.filter(email=email)
        if user.exists():
            send_otp_for_password_reset(email)
            return redirect('reset-password')
        else:
            messages.error(request, "Email not found")
            return render(request, 'forgot-password.html')
    return render(request, 'forgot-password.html')

def reset_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        password = request.POST.get('password')
        
        if not token or not password:
            messages.error(request, "OTP and password are required.")
            return render(request, 'password-reset.html')

        try:
            instance = OneTimePassword.objects.get(code=token)
        except OneTimePassword.DoesNotExist:
            messages.error(request, "Invalid OTP.")
            return render(request, 'password-reset.html')

        if instance.is_valid:
            user = instance.user
            user.set_password(password)
            user.save()
            instance.delete()  # Delete OTP from the database after successful validation
            messages.success(request, "Password reset successfully.")
            return redirect('login')
        else:
            messages.error(request, "OTP is not valid or has expired.")
    
    return render(request, 'password-reset.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def contact(request):
    return render(request, "contact.html")

def products(request, category_id=None):

    query = request.GET.get('q')

    categories = Category.objects.all()
    drugs = Drug.objects.all()

    if query:
        drugs = drugs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
    if category_id:
        try:
            category = Category.objects.get(pk=category_id)
            drugs = drugs.filter(category=category)
        except Category.DoesNotExist:
            # Handle case where category ID is invalid (optional)
            pass

    paginator = Paginator(drugs, 9)  # Show 9 drugs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'drugs': drugs,
        'page_obj': page_obj,
    }

    return render(request, "products.html", context)


def services(request):
    return render(request, "services.html")


def item_view(request, id):
    drug = get_object_or_404(Drug, id=id)
    return render(request, 'item.html', {'drug': drug})


def cart_view(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate subtotal for each cart item and the total for the cart
    cart_items_with_subtotal = []
    total = 0
    for item in cart_items:
        subtotal = item.drug.price * item.quantity
        total += subtotal
        cart_items_with_subtotal.append({
            'item': item,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items_with_subtotal': cart_items_with_subtotal,
        'total': total,
    })


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Use the session key to identify the cart for an anonymous user
        if 'cart_id' in request.session:
            cart_id = request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
        else:
            # Create a new cart and store its ID in the session
            cart = Cart.objects.create(user=None)
            request.session['cart_id'] = cart.id
    return cart

def add_to_cart(request, drug_id):
    cart = get_cart(request)
    drug = get_object_or_404(Drug, id=drug_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, drug=drug)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart-view')

def subtract_from_cart(request, drug_id):
    cart = get_cart(request)
    drug = get_object_or_404(Drug, id=drug_id)
    cart_item = get_object_or_404(CartItem, cart=cart, drug=drug)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart-view')


def remove_from_cart(request, drug_id):
    cart = get_cart(request)
    drug = get_object_or_404(Drug, id=drug_id)
    cart_item = CartItem.objects.filter(cart=cart, drug=drug).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart-view')


def about(request):
    return render(request, 'about.html')


def create_checkout_session(request):    
    if request.method == "POST":
        user = request.user
        # Logic to get cart items of the user
        cart_items = CartItem.objects.filter(cart__user=user)
        
        # Prepare line items for Stripe Checkout
        line_items = []
        for cart_item in cart_items:
            line_items.append({
                'price': cart_item.drug.price_id,  # Assuming each drug has a 'price_id' field
                'quantity': cart_item.quantity,
            })

        
        # Get billing info from the form
        name = request.POST.get("name")
        delivery_address = request.POST.get('address')
        contact = request.POST.get("tel")
    
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=f"{settings.DOMAIN}/success",
                cancel_url=f"{settings.DOMAIN}/cancel",
            )

            # Redirect to the Stripe checkout page if the session creation is successful
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            # Handle errors
            error_message = str(e)
            messages.error(request, error_message)
            return render(request, 'checkout.html', {'error': error_message})
    else:
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Please sign in to complete your order")
            return redirect('login')

        return render(request, 'checkout.html')  # Render the checkout form


def success_view(request):
    user = request.user
    cart = get_cart(request)
    
    # Clear the user's cart items
    CartItem.objects.filter(cart=cart).delete()
    return render(request, 'success.html')

def cancel_view(request):
    return render(request, 'cancel.html')