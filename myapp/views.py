from django.shortcuts import render, get_object_or_404 , redirect
from .models import Category
from .models import Product,SubCategory
from .cart import Cart


from .models import Category, Product

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


def shop(request):
    return render(request, "shop.html")


def blog(request):
    return render(request, "blog.html")


def contact(request):
    return render(request, "contact.html")


def checkout(request):
    return render(request, "checkout.html")

# cart sectionn start

def cart(request):

    cart = Cart(request)

    context = {
        "cart": cart,
        "total": cart.get_total_price(),
    }

    return render(request, "shop-cart.html", context)
def add_to_cart(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    cart = Cart(request)

    cart.add(product)

    return redirect("cart")
def remove_from_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = Cart(request)

    cart.remove(product)

    return redirect("cart")
def increase_quantity(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = Cart(request)

    cart.add(product)

    return redirect("cart")
def decrease_quantity(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = Cart(request)

    cart.decrease(product)

    return redirect("cart")

    # cart section
    

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
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "product-details.html", context)


def blog_details(request):
    return render(request, "blog-details.html")


def women(request):

    products = Product.objects.filter(
        category__slug="women",
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="women"
    )

    context = {
        "products": products,
        "subcategories": subcategories,
    }

    return render(request, "women.html", context)



def women_subcategory(request, subcategory_slug):

    products = Product.objects.filter(
        category__slug="women",
        subcategory__slug=subcategory_slug,
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="women"
    )

    context = {
        "products": products,
        "subcategories": subcategories,
    }

    return render(request, "women.html", context)

from .models import Product, SubCategory

def men(request):

    products = Product.objects.filter(
        category__slug="men",
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="men"
    )

    context = {
        "products": products,
        "subcategories": subcategories,
    }

    return render(request, "men.html", context)
def men_subcategory(request, subcategory_slug):

    products = Product.objects.filter(
        category__slug="men",
        subcategory__slug=subcategory_slug,
        is_available=True
    )

    subcategories = SubCategory.objects.filter(
        category__slug="men"
    )

    context = {
        "products": products,
        "subcategories": subcategories,
    }

    return render(request, "men.html", context)


def wishlist(request):
    return render(request, "wishlist.html")


def liked(request):
    return render(request, "liked.html")


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")
def base(request):
    return render(request, "base.html")

