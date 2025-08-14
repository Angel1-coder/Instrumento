from django.contrib import admin
from .models import Category, InstrumentType, Product, Accessory, SubscriptionPlan, InsuranceOption, RentalOrder


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'instrument_type', 'brand', 'model',
        'rental_price_6months', 'purchase_price', 'stock_quantity', 'is_active'
    ]
    list_editable = ['is_active', 'stock_quantity']
    list_filter = ['category', 'instrument_type', 'is_rental_available', 'is_purchase_available', 'is_active']
    search_fields = ['name', 'brand', 'model', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'long_description', 'category', 'instrument_type')
        }),
        ('Product Details', {
            'fields': ('brand', 'model', 'condition', 'year_made', 'stock_quantity')
        }),
        ('Rental Pricing', {
            'fields': (
                'rental_price_3months', 'rental_price_6months', 
                'rental_price_12months', 'rental_price_24months',
                'is_rental_available'
            )
        }),
        ('Purchase & Insurance', {
            'fields': (
                'purchase_price', 'is_purchase_available',
                'basic_insurance_monthly', 'premium_insurance_monthly'
            )
        }),
        ('Student Benefits', {
            'fields': ('student_discount_percentage',)
        }),
        ('Media & Content', {
            'fields': ('image', 'image_url', 'sound_sample_url', 'video_url')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')


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


@admin.register(RentalOrder)
class RentalOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'product', 'rental_duration', 
        'monthly_price', 'total_price', 'status', 'created_at'
    ]
    list_filter = ['status', 'rental_duration', 'insurance_type', 'created_at']
    search_fields = ['order_number', 'user__username', 'product__name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'product', 'status')
        }),
        ('Rental Details', {
            'fields': ('rental_duration', 'start_date', 'end_date')
        }),
        ('Pricing', {
            'fields': (
                'monthly_price', 'total_price', 'student_discount_applied', 
                'discount_amount'
            )
        }),
        ('Insurance & Services', {
            'fields': ('insurance_type', 'insurance_cost', 'includes_lessons', 'lesson_cost')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        })
    )
    
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')



