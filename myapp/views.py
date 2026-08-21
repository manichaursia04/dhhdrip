from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect

from .models import (
    Category,
    Product,
    SubCategory,
    Order,
    OrderItem,
)
#for login
from .cart import Cart
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout

# =========================================================
# HOME
# =========================================================

def home(request):

    women = Category.objects.get(slug="women")
    men = Category.objects.get(slug="men")
    kids = Category.objects.get(slug="kids")
    cosmetics = Category.objects.get(slug="cosmetics")
    accessories = Category.objects.get(slug="accessories")

    products = Product.objects.filter(
        is_home=True,
        is_available=True
    )

    context = {
        "women": women,
        "men": men,
        "kids": kids,
        "cosmetics": cosmetics,
        "accessories": accessories,
        "products": products,
    }

    return render(request, "home.html", context)


# =========================================================
# BASIC PAGES
# =========================================================

def shop(request):
    return render(request, "shop.html")


def blog(request):
    return render(request, "blog.html")


def contact(request):
    return render(request, "contact.html")


# =========================================================
# CHECKOUT
# =========================================================

@login_required(login_url="login")
def checkout(request):

    cart = Cart(request)

    # Don't allow checkout with an empty cart
    if not cart.cart:
        return redirect("cart")

    # =====================================================
    # POST - PLACE ORDER
    # =====================================================

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        country = request.POST.get("country")
        address = request.POST.get("address")
        apartment = request.POST.get("apartment", "")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        order_notes = request.POST.get("order_notes", "")

        # Calculate totals on server
        subtotal = cart.get_total_price()

        tax = subtotal * Decimal("0.18")

        handling_fee = Decimal("20.00")

        total = subtotal + tax + handling_fee

        # =====================================================
        # CREATE ORDER
        # =====================================================

        order = Order.objects.create(

            # IMPORTANT
            # Connect order to logged-in customer
            user=request.user,

            first_name=first_name,
            last_name=last_name,

            country=country,
            address=address,
            apartment=apartment,

            city=city,
            state=state,
            postcode=postcode,

            phone=phone,
            email=email,

            order_notes=order_notes,

            subtotal=subtotal,
            tax=tax,
            handling_fee=handling_fee,
            total=total,

            status="Pending",
        )

        # =====================================================
        # CREATE ORDER ITEMS
        # =====================================================

        for item in cart:

            OrderItem.objects.create(
                order=order,
                product=item["product"],
                product_name=item["product"].name,
                size=item.get("size", ""),
                price=item["price"],
                quantity=item["quantity"],
                total=item["total"],
            )

        # Empty cart
        cart.clear()

        # Go to success page
        return redirect(
            "order_success",
            order_id=order.id
        )

    # =====================================================
    # GET - SHOW CHECKOUT
    # =====================================================

    subtotal = cart.get_total_price()

    tax = subtotal * Decimal("0.18")

    handling_fee = Decimal("20.00")

    total = subtotal + tax + handling_fee

    context = {
        "cart": cart,
        "subtotal": subtotal,
        "tax": tax,
        "handling_fee": handling_fee,
        "total": total,
    }

    return render(
        request,
        "checkout.html",
        context
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

@login_required(login_url="login")
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "order-success.html",
        {
            "order": order
        }
    )


# =========================================================
# CART
# =========================================================

def cart(request):

    cart = Cart(request)

    context = {
        "cart": cart,
        "total": cart.get_total_price(),
    }

    return render(
        request,
        "shop-cart.html",
        context
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    # Selected size from product page
    size = request.POST.get("size")

    # Selected quantity
    try:

        quantity = int(
            request.POST.get(
                "quantity",
                1
            )
        )

        if quantity < 1:
            quantity = 1

    except (TypeError, ValueError):

        quantity = 1

    cart = Cart(request)

    cart.add(
        product,
        size,
        quantity
    )

    return redirect("cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(request, cart_key):

    cart = Cart(request)

    cart.remove(cart_key)

    return redirect("cart")


# =========================================================
# INCREASE QUANTITY
# =========================================================

def increase_quantity(request, cart_key):

    cart = Cart(request)

    item = cart.cart.get(cart_key)

    if item:

        product = get_object_or_404(
            Product,
            id=item["product_id"]
        )

        cart.add(
            product,
            item["size"],
            1
        )

    return redirect("cart")


# =========================================================
# DECREASE QUANTITY
# =========================================================

def decrease_quantity(request, cart_key):

    cart = Cart(request)

    cart.decrease(cart_key)

    return redirect("cart")


# =========================================================
# PRODUCT DETAILS
# =========================================================

def product_details(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    print(product.name)
    print(product.price)
    print(product.category.name)

    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(
        id=product.id
    )[:4]

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(
        request,
        "product-details.html",
        context
    )


# =========================================================
# BLOG DETAILS
# =========================================================

def blog_details(request):

    return render(
        request,
        "blog-details.html"
    )


# =========================================================
# WOMEN
# =========================================================

def women(request):

    products = Product.objects.filter(
        category__slug="women",
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="women"
    )

    # Size filter
    size = request.GET.get("size")

    if size:

        products = products.filter(
            sizes__name__iexact=size
        )

    context = {
        "products": products,
        "subcategories": subcategories,
        "selected_size": size,
    }

    return render(
        request,
        "women.html",
        context
    )


# =========================================================
# WOMEN SUBCATEGORY
# =========================================================

def women_subcategory(request, subcategory_slug):

    products = Product.objects.filter(
        category__slug="women",
        subcategory__slug=subcategory_slug,
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="women"
    )

    # Size filter
    size = request.GET.get("size")

    if size:

        products = products.filter(
            sizes__name__iexact=size
        )

    context = {
        "products": products,
        "subcategories": subcategories,
        "selected_size": size,
    }

    return render(
        request,
        "women.html",
        context
    )


# =========================================================
# MEN
# =========================================================

def men(request):

    products = Product.objects.filter(
        category__slug="men",
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="men"
    )

    # Size filter
    size = request.GET.get("size")

    if size:

        products = products.filter(
            sizes__name__iexact=size
        )

    context = {
        "products": products,
        "subcategories": subcategories,
        "selected_size": size,
    }

    return render(
        request,
        "men.html",
        context
    )


# =========================================================
# MEN SUBCATEGORY
# =========================================================

def men_subcategory(request, subcategory_slug):

    products = Product.objects.filter(
        category__slug="men",
        subcategory__slug=subcategory_slug,
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="men"
    )

    # Size filter
    size = request.GET.get("size")

    if size:

        products = products.filter(
            sizes__name__iexact=size
        )

    context = {
        "products": products,
        "subcategories": subcategories,
        "selected_size": size,
    }

    return render(
        request,
        "men.html",
        context
    )


# =========================================================
# OTHER PAGES
# =========================================================

def wishlist(request):

    return render(
        request,
        "wishlist.html"
    )


def liked(request):

    return render(
        request,
        "liked.html"
    )


def login(request):

    if request.user.is_authenticated:
        return redirect("home")

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = User.objects.filter(email__iexact=email).first()

        if user is not None:

            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:

                auth_login(request, authenticated_user)

                if next_url:
                    return redirect(next_url)

                return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid email or password.",
                "next": next_url,
            }
        )

    return render(
        request,
        "login.html",
        {
            "next": next_url,
        }
    )




def base(request):

    return render(
        request,
        "base.html"
    )
def logout(request):

    auth_logout(request)

    return redirect("home")



#otp code setup

from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login
import random
import time

def register(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(
                request,
                "An account with this email already exists."
            )
            return redirect("register")

        # Generate 6 digit OTP
        verification_code = str(
            random.randint(100000, 999999)
        )

        # Store registration information temporarily
        request.session["registration_data"] = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }

        # Store OTP
        request.session["verification_code"] = verification_code

        # OTP expiry time: 10 minutes
        request.session["verification_expiry"] = (
            time.time() + 600
        )

        # Send verification email
        send_mail(
            "Verify your email - Your Store",
            f"""
Hello {first_name},

Your email verification code is:

{verification_code}

This code will expire in 10 minutes.

If you did not create an account, you can ignore this email.

Thank you.
""",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Verification code sent to your email."
        )

        return redirect("verify_email")

    return render(request, "register.html")

def verify_email(request):

    if "registration_data" not in request.session:
        messages.error(
            request,
            "Your registration session has expired. Please register again."
        )
        return redirect("register")

    if request.method == "POST":

        entered_code = request.POST.get(
            "verification_code"
        )

        saved_code = request.session.get(
            "verification_code"
        )

        expiry = request.session.get(
            "verification_expiry"
        )

        # Check expiry
        if not expiry or time.time() > expiry:

            request.session.pop(
                "verification_code",
                None
            )

            request.session.pop(
                "verification_expiry",
                None
            )

            messages.error(
                request,
                "Verification code expired. Please register again."
            )

            return redirect("register")

        # Check OTP
        if entered_code != saved_code:

            messages.error(
                request,
                "Invalid verification code."
            )

            return redirect("verify_email")

        # Get registration information
        registration_data = request.session.get(
            "registration_data"
        )

        # Create user
        user = User.objects.create_user(
            username=registration_data["email"],
            email=registration_data["email"],
            password=registration_data["password"],
            first_name=registration_data["first_name"],
            last_name=registration_data["last_name"],
        )

        # Remove temporary registration data
        request.session.pop(
            "registration_data",
            None
        )

        request.session.pop(
            "verification_code",
            None
        )

        request.session.pop(
            "verification_expiry",
            None
        )

        messages.success(
            request,
            "Email verified successfully. You can now login."
        )

        return redirect("login")

    return render(
        request,
        "verify-email.html"
    )