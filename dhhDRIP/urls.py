"""
URL configuration for dhhDRIP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)