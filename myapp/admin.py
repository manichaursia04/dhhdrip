from django.contrib import admin
from .models import Category , Product,SubCategory,Size

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)} 
    filter_horizontal = ("sizes",) 

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
   

admin.site.register(Category)
admin.site.register(Size)