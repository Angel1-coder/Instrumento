from django.db import models


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
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    long_description = models.TextField(null=True, blank=True)
    
    # Product options
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    is_rental_available = models.BooleanField(default=True)
    is_purchase_available = models.BooleanField(default=True)
    
    # Pricing
    rental_price_monthly = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Product details
    brand = models.CharField(max_length=254, null=True, blank=True)
    model = models.CharField(max_length=254, null=True, blank=True)
    condition = models.CharField(max_length=50, null=True, blank=True)  # New, Used, Vintage
    year_made = models.IntegerField(null=True, blank=True)
    
    # Media
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    sound_sample_url = models.URLField(max_length=1024, null=True, blank=True)
    video_url = models.URLField(max_length=1024, null=True, blank=True)
    
    # Ratings and reviews
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    review_count = models.IntegerField(default=0)
    
    # Availability
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['category', 'instrument_type', 'name']

    def __str__(self):
        return self.name

    def get_rental_price_display(self):
        if self.rental_price_monthly:
            return f"€{self.rental_price_monthly}/month"
        return "Rental not available"

    def get_purchase_price_display(self):
        if self.purchase_price:
            return f"€{self.purchase_price}"
        return "Purchase not available"


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
