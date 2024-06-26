from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import User, OneTimePassword, Drug, Category, Cart, CartItem, BlogPost
from .utils import send_otp_for_password_reset
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import os
import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create your views here.
def index(request):
    categories = Category.objects.all()
    best_sellers = Drug.objects.filter(best_sellers__gt=0)  # Filter drugs with best_sellers > 0

    context = {
        'categories': categories,
        'best_sellers': best_sellers,
        'current_page': 'home'

    }
    return render(request, 'index.html', context)


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
                
                messages.success(request, _("Login successful!"))
                return redirect("index")
            else:
                messages.error(request, _("Invalid email or password."))
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = UserLoginForm()
    
    return render(request, "login.html", {"form": form,'current_page': 'login'})


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _("Registration successful. You can now log in."))
            return redirect("login")
        else:
            messages.error(request, _("Registration failed. Please correct the errors below."))
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form, 'current_page': 'register'})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        if not email:
            messages.error(request, _('Email is required'))
            return render(request, 'forgot-password.html')
        user = User.objects.filter(email=email)
        if user.exists():
            send_otp_for_password_reset(email)
            return redirect('reset-password')
        else:
            messages.error(request, _("Email not found"))
            return render(request, 'forgot-password.html')
    return render(request, 'forgot-password.html')

def reset_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        password = request.POST.get('password')
        
        if not token or not password:
            messages.error(request, _("OTP and password are required."))
            return render(request, 'password-reset.html')

        try:
            instance = OneTimePassword.objects.get(code=token)
        except OneTimePassword.DoesNotExist:
            messages.error(request, _("Invalid OTP."))
            return render(request, 'password-reset.html')

        if instance.is_valid:
            user = instance.user
            user.set_password(password)
            user.save()
            instance.delete()  # Delete OTP from the database after successful validation
            messages.success(request, _("Password reset successfully."))
            return redirect('login')
        else:
            messages.error(request, _("OTP is not valid or has expired."))
    
    return render(request, 'password-reset.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def contact(request):
    context = {
        'name_placeholder': _('Name'),
        'email_placeholder': _('Email'),
        'message_placeholder': _('Message'),
        'phone_number_placeholder': _('Phone Number'),
        'name_of_medication_placeholder': _('Name Of Medication'),
        'medication_use_placeholder': _('What is the medication used for'),
        'current_page': 'contact'

    }
    return render(request, "contact.html", context)

def products(request, category_id=None):

    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'name')  # Default sorting by drug name
    categories = Category.objects.all()
    
    # Retrieve all drugs initially
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


    # Sort drugs based on selected sorting option
    if sort_by == 'price_low_to_high':
        drugs = drugs.order_by('price')
    elif sort_by == 'price_high_to_low':
        drugs = drugs.order_by('-price')
    elif sort_by == 'popularity':
        drugs = drugs.filter(best_sellers__gte=0).order_by('-best_sellers')
    else:
        # Default sorting by drug name
        drugs = drugs.order_by('name')

    #pagination
    paginator = Paginator(drugs, 9)  # Show 9 drugs per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'drugs': drugs,
        'page_obj': page_obj,
        'current_page': 'products'
    }

    return render(request, "products.html", context)


def services(request):
    return render(request, "services.html", {'current_page': 'services'})


def faqs(request):
    return render(request, "frequent-questions.html", {'current_page': 'faqs'})


def blog(request):
    tag_slug = request.GET.get('tag')
    page_number = request.GET.get('page')
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = BlogPost.objects.filter(tags=tag).order_by('created_at')
    else:
        posts = BlogPost.objects.all().order_by('created_at')
        tag = None  # If no tag is selected
    
    paginator = Paginator(posts, 5)  # Show 5 blog posts per page
    page_obj = paginator.get_page(page_number)
    all_tags = Tag.objects.all()

    context = {
        'posts': page_obj,
        'tag': tag_slug,
        'page_obj': page_obj,
        'all_tags': all_tags,
        'selected_tag': tag_slug,
        'current_page': 'blog'

    }
    
    return render(request, 'blog.html', context)


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    previous_post = BlogPost.objects.filter(id__lt=post.id).order_by('-id').first()
    next_post = BlogPost.objects.filter(id__gt=post.id).order_by('id').first()

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'current_page': 'blog'
    }
    return render(request, 'blog-detail.html', context)


def item_view(request, id):
    drug = get_object_or_404(Drug, id=id)
    return render(request, 'item.html', {'drug': drug, 'current_page': 'products'})


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
    return render(request, 'about.html', {'current_page': 'about'})


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
            messages.error(request, _("Please sign in to complete your order"))
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