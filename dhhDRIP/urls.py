from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('women/', views.women, name='women'),
    path("women/<slug:subcategory_slug>/",
    views.women_subcategory,
    name="women_subcategory",
), 
    path('men/', views.men, name='men'),
    path("men/<slug:subcategory_slug>/",
    views.men_subcategory,
    name="men_subcategory",
),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),

    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),

    path(
    "product/<slug:slug>/",
    views.product_details,
    name="product-details",
),
    path('blog-details/', views.blog_details, name='blog-details'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('liked/', views.liked, name='liked'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path(
    "add-to-cart/<slug:slug>/",
    views.add_to_cart,
    name="add_to_cart",
),

path(
    "cart/remove/<str:cart_key>/",
    views.remove_from_cart,
    name="remove_from_cart",
),

path(
    "cart/increase/<str:cart_key>/",
    views.increase_quantity,
    name="increase_quantity",
),

path(
    "cart/decrease/<str:cart_key>/",
    views.decrease_quantity,
    name="decrease_quantity",
),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
