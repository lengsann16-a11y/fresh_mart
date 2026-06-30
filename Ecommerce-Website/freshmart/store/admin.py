from django.contrib import admin
from .models import Category, Product, Order, OrderItem, CustomerProfile


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'old_price', 'stock', 'available', 'is_featured', 'created']
    list_filter = ['available', 'is_featured', 'is_organic', 'category', 'created']
    list_editable = ['price', 'stock', 'available', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_number', 'first_name', 'last_name', 'email', 'paid', 'status', 'created']
    list_filter = ['paid', 'status', 'created']
    list_editable = ['paid', 'status']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
    date_hierarchy = 'created'


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city']
    search_fields = ['user__username', 'user__email']