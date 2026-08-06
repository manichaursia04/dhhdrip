from django.db import models
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

  
