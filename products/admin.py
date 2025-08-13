from django.contrib import admin
from .models import Category, InstrumentType, Product, Accessory, SubscriptionPlan, InsuranceOption


class InstrumentTypeInline(admin.TabularInline):
    model = InstrumentType
    extra = 1
    fields = ('name', 'description', 'image', 'display_order', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'friendly_name')
    inlines = [InstrumentTypeInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'friendly_name', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon', 'display_order', 'is_active')
        }),
    )


@admin.register(InstrumentType)
class InstrumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'category__name')
    ordering = ('category', 'display_order')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'instrument_type', 'brand', 'model', 
                   'rental_price_monthly', 'purchase_price', 'stock_quantity', 'is_active')
    list_editable = ('is_active', 'stock_quantity')
    list_filter = ('category', 'instrument_type', 'is_rental_available', 
                  'is_purchase_available', 'condition', 'is_active')
    search_fields = ('name', 'brand', 'model', 'description')
    ordering = ('category', 'instrument_type', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'instrument_type', 'description', 'long_description')
        }),
        ('Product Details', {
            'fields': ('brand', 'model', 'condition', 'year_made', 'sku')
        }),
        ('Pricing & Options', {
            'fields': ('rental_price_monthly', 'purchase_price', 'is_rental_available', 
                      'is_purchase_available', 'has_sizes')
        }),
        ('Media', {
            'fields': ('image', 'image_url', 'sound_sample_url', 'video_url')
        }),
        ('Availability', {
            'fields': ('stock_quantity', 'is_active')
        }),
    )


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active')
    list_editable = ('price', 'stock_quantity', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'monthly_price', 'total_price', 
                   'discount_percentage', 'is_popular', 'is_active')
    list_editable = ('monthly_price', 'discount_percentage', 'is_popular', 'is_active')
    list_filter = ('duration_months', 'is_popular', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('duration_months',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'duration_months', 'description')
        }),
        ('Pricing', {
            'fields': ('monthly_price', 'discount_percentage')
        }),
        ('Features', {
            'fields': ('features', 'is_popular', 'is_active')
        }),
    )


@admin.register(InsuranceOption)
class InsuranceOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_cost', 'coverage_amount', 'deductible', 'is_active')
    list_editable = ('monthly_cost', 'coverage_amount', 'deductible', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)


# Register the Product model with the custom admin
admin.site.register(Product, ProductAdmin)
