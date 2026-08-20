from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ===========================
# Category Model
# ===========================

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/')
    description = models.TextField(blank=True)
    item_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# ===========================
# Sub Category Model
# ===========================

class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

# for size model 
class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
#size model end here
# ===========================
# Product Model
# ===========================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE
    )
    sizes = models.ManyToManyField(Size, blank=True)
    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    image = models.ImageField(upload_to='products/')

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    is_new = models.BooleanField(default=False)

    is_sale = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Order Model

class Order(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    address = models.CharField(max_length=255)
    apartment = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    postcode = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)
    email = models.EmailField()

    order_notes = models.TextField(
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    handling_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default="Pending"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"
# ===========================
# Order Item Model
# ===========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    product_name = models.CharField(
        max_length=200
    )

    size = models.CharField(
        max_length=10
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product_name} - {self.size}"