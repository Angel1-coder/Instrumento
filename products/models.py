from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    """
    Main instrument category (e.g., Strings, Percussion, Keys, Wind, Wellness)
    """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)  # FontAwesome icon
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class InstrumentType(models.Model):
    """
    Specific instrument type within a category (e.g., Electric Guitar, Acoustic Guitar)
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='instrument_types')
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Product(models.Model):
    """
    Individual instrument product with rental/subscription options
    """
    INSTRUMENT_TYPE_CHOICES = [
        ('rental', 'Rental Only'),
        ('purchase', 'Purchase Only'),
        ('both', 'Rental & Purchase'),
    ]

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    instrument_type = models.ForeignKey(InstrumentType, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    long_description = models.TextField(blank=True, null=True)
    is_rental_available = models.BooleanField(default=True)
    is_purchase_available = models.BooleanField(default=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True)
    year_made = models.IntegerField(blank=True, null=True)
    sound_sample_url = models.URLField(max_length=1024, blank=True, null=True)
    video_url = models.URLField(max_length=1024, blank=True, null=True)
    review_count = models.IntegerField(default=0)
    stock_quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # Rental pricing for different durations
    rental_price_3months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rental_price_6months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rental_price_12months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rental_price_24months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Purchase price
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Student discount
    student_discount_percentage = models.IntegerField(default=10, help_text="Student discount in percentage")
    
    # Insurance options
    basic_insurance_monthly = models.DecimalField(max_digits=6, decimal_places=2, default=9.99)
    premium_insurance_monthly = models.DecimalField(max_digits=6, decimal_places=2, default=14.99)
    
    # Image fields
    image = models.ImageField(upload_to='', null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_rental_price(self, duration_months, is_student=False):
        """Get rental price for specific duration with optional student discount"""
        price_map = {
            3: self.rental_price_3months,
            6: self.rental_price_6months,
            12: self.rental_price_12months,
            24: self.rental_price_24months
        }
        
        base_price = price_map.get(duration_months)
        if not base_price:
            return None
            
        if is_student:
            discount = (self.student_discount_percentage / 100) * base_price
            return base_price - discount
        
        return base_price
    
    def get_total_rental_cost(self, duration_months, is_student=False):
        """Get total cost for entire rental period"""
        monthly_price = self.get_rental_price(duration_months, is_student)
        if monthly_price:
            return monthly_price * duration_months
        return None
    
    def get_insurance_cost(self, insurance_type, duration_months):
        """Get total insurance cost for rental period"""
        if insurance_type == 'basic':
            return self.basic_insurance_monthly * duration_months
        elif insurance_type == 'premium':
            return self.premium_insurance_monthly * duration_months
        return 0


class Accessory(models.Model):
    """
    Musical accessories like picks, straps, cables, cases
    """
    ACCESSORY_CATEGORIES = [
        ('picks', 'Picks & Plectrums'),
        ('straps', 'Straps & Harnesses'),
        ('cables', 'Cables & Connectors'),
        ('cases', 'Cases & Bags'),
        ('stands', 'Stands & Holders'),
        ('maintenance', 'Maintenance & Care'),
        ('other', 'Other Accessories'),
    ]

    category = models.CharField(max_length=50, choices=ACCESSORY_CATEGORIES)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Accessories'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"


class SubscriptionPlan(models.Model):
    """
    Rental subscription plans (3, 6, 12, 24 months)
    """
    DURATION_CHOICES = [
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '12 Months'),
        (24, '24 Months'),
    ]

    name = models.CharField(max_length=254)
    duration_months = models.IntegerField(choices=DURATION_CHOICES)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_popular = models.BooleanField(default=False)
    description = models.TextField()
    features = models.TextField(help_text="List of features included in this plan")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['duration_months']

    def __str__(self):
        return f"{self.name} ({self.duration_months} months)"

    def save(self, *args, **kwargs):
        # Calculate total price based on monthly price and duration
        self.total_price = self.monthly_price * self.duration_months
        super().save(*args, **kwargs)


class InsuranceOption(models.Model):
    """
    Insurance options for instruments
    """
    name = models.CharField(max_length=254)
    description = models.TextField()
    monthly_cost = models.DecimalField(max_digits=8, decimal_places=2)
    coverage_amount = models.DecimalField(max_digits=8, decimal_places=2)
    deductible = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RentalOrder(models.Model):
    """Model for rental orders/subscriptions"""
    
    RENTAL_DURATIONS = [
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '12 Months'),
        (24, '24 Months'),
    ]
    
    INSURANCE_CHOICES = [
        ('none', 'No Insurance'),
        ('basic', 'Basic Insurance'),
        ('premium', 'Premium Insurance'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Order details
    order_number = models.CharField(max_length=32, null=False, editable=False, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='rental_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rental_orders')
    
    # Rental details
    rental_duration = models.IntegerField(choices=RENTAL_DURATIONS)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Pricing
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    student_discount_applied = models.BooleanField(default=False)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Insurance
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_CHOICES, default='none')
    insurance_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Additional services
    includes_lessons = models.BooleanField(default=True)
    lesson_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rental Order {self.order_number} - {self.product.name}"
    
    def save(self, *args, **kwargs):
        """Generate order number if not set"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
    
    def _generate_order_number(self):
        """Generate unique order number"""
        import uuid
        return f"RENTAL-{uuid.uuid4().hex[:8].upper()}"
    
    def calculate_total_price(self):
        """Calculate total price including all costs"""
        base_cost = self.monthly_price * self.rental_duration
        total = base_cost + self.insurance_cost + self.lesson_cost - self.discount_amount
        return max(total, 0)  # Ensure total is not negative
    
    def get_remaining_days(self):
        """Get remaining days in rental period"""
        from datetime import date
        today = date.today()
        if today <= self.end_date:
            return (self.end_date - today).days
        return 0
    
    def can_cancel(self):
        """Check if rental can be cancelled"""
        return self.status in ['pending', 'active'] and self.get_remaining_days() > 0
    
    def can_pause(self):
        """Check if rental can be paused"""
        return self.status == 'active' and self.get_remaining_days() > 30
