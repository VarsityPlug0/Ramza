from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import os

class ContentSection(models.Model):
    """Manage all text content on the website"""
    SECTION_CHOICES = [
        ('home_hero', 'Home - Hero Section'),
        ('home_features', 'Home - Features Section'),
        ('home_cta', 'Home - Call to Action'),
        ('menu_hero', 'Menu - Hero Section'),
        ('footer', 'Footer Content'),
        ('navigation', 'Navigation'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
        ('checkout', 'Checkout Page'),
        ('cart', 'Cart Page'),
    ]
    
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=200, blank=True, help_text="Main heading/title")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Subtitle or tagline")
    description = models.TextField(blank=True, help_text="Main content/description")
    button_text = models.CharField(max_length=100, blank=True, help_text="Button text if applicable")
    button_url = models.CharField(max_length=200, blank=True, help_text="Button URL if applicable")
    
    # Additional text fields for complex sections
    extra_text_1 = models.TextField(blank=True, help_text="Additional text field 1")
    extra_text_2 = models.TextField(blank=True, help_text="Additional text field 2")
    extra_text_3 = models.TextField(blank=True, help_text="Additional text field 3")
    
    # Image fields
    image = models.ImageField(upload_to='content/', blank=True, null=True, help_text="Main image for this section")
    background_image = models.ImageField(upload_to='content/backgrounds/', blank=True, null=True, help_text="Background image")
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True, help_text="Page title for SEO")
    meta_description = models.TextField(blank=True, help_text="Page description for SEO")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['section']
        verbose_name = 'Content Section'
        verbose_name_plural = 'Content Sections'
    
    def __str__(self):
        return f"{self.get_section_display()}"

class SiteImage(models.Model):
    """Manage all images used throughout the site"""
    IMAGE_TYPES = [
        ('logo', 'Logo'),
        ('hero', 'Hero Images'),
        ('background', 'Background Images'),
        ('category', 'Category Images'),
        ('menu_item', 'Menu Item Images'),
        ('gallery', 'Gallery Images'),
        ('icon', 'Icons'),
        ('other', 'Other Images'),
    ]
    
    name = models.CharField(max_length=200, help_text="Descriptive name for this image")
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='other')
    image = models.ImageField(upload_to='site_images/', help_text="Upload image file")
    alt_text = models.CharField(max_length=200, help_text="Alt text for accessibility")
    description = models.TextField(blank=True, help_text="Description of the image")
    
    # Where this image is used
    used_in_sections = models.ManyToManyField(ContentSection, blank=True, help_text="Which content sections use this image")
    
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['image_type', 'sort_order', 'name']
        verbose_name = 'Site Image'
        verbose_name_plural = 'Site Images'
    
    def __str__(self):
        return f"{self.name} ({self.get_image_type_display()})"
    
    @property
    def file_size(self):
        if self.image and hasattr(self.image, 'size'):
            return self.image.size
        return 0
    
    @property
    def file_size_mb(self):
        size = self.file_size
        return round(size / (1024 * 1024), 2) if size else 0

class Category(models.Model):
    name = models.CharField(max_length=100, help_text="Category name (e.g., Burgers, Pizzas)")
    description = models.TextField(blank=True, help_text="Brief description of this category")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text="Category display image (recommended: 400x300px)")
    is_active = models.BooleanField(default=True, help_text="Show this category on the menu")
    sort_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def item_count(self):
        return self.menu_items.filter(is_available=True).count()
    item_count.short_description = 'Available Items'

class MenuItem(models.Model):
    name = models.CharField(max_length=200, help_text="Item name as it appears on the menu")
    description = models.TextField(help_text="Detailed description for customers")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in Rand (e.g., 12.99)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items', help_text="Which category this item belongs to")
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True, help_text="Food photo (recommended: 600x400px)")
    is_available = models.BooleanField(default=True, help_text="Show this item on the menu")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage as featured item")
    ingredients = models.TextField(blank=True, help_text="Comma-separated list of ingredients")
    preparation_time = models.IntegerField(default=15, help_text="Preparation time in minutes")
    stock_quantity = models.IntegerField(default=100, help_text="Current stock level (0 = out of stock)")
    low_stock_threshold = models.IntegerField(default=10, help_text="Alert when stock falls below this number")
    calories = models.IntegerField(blank=True, null=True, help_text="Calories per serving (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} - R{self.price}'

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        return self.stock_quantity <= 0

    def reduce_stock(self, quantity=1):
        """Reduce stock when item is ordered"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False

class SiteSettings(models.Model):
    """Global site settings that admin can modify"""
    # Basic Site Info
    site_name = models.CharField(max_length=100, default="Ramza's Chillas", help_text="Restaurant name displayed on site")
    site_description = models.TextField(default="Chill Vibes • Hot Food", help_text="Tagline for your restaurant")
    
    # Contact Information
    phone_number = models.CharField(max_length=20, default="(555) 123-CHILL", help_text="Restaurant phone number")
    email = models.EmailField(default="hello@ramzaschillas.com", help_text="Restaurant email")
    address = models.TextField(default="123 Chill Street, Island City", help_text="Restaurant address")
    
    # Social Media
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter page URL")
    
    # Business Hours
    opening_time = models.TimeField(default='09:00', help_text="Daily opening time")
    closing_time = models.TimeField(default='22:00', help_text="Daily closing time")
    business_hours_text = models.TextField(default="Mon-Thu: 11:00 AM - 10:00 PM\nFri-Sat: 11:00 AM - 11:00 PM\nSunday: 12:00 PM - 9:00 PM", help_text="Detailed business hours display")
    
    # Delivery Settings
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=3.99, help_text="Standard delivery fee")
    free_delivery_minimum = models.DecimalField(max_digits=8, decimal_places=2, default=25.00, help_text="Minimum order for free delivery")
    delivery_radius = models.IntegerField(default=5, help_text="Delivery radius in kilometers")
    delivery_time_text = models.CharField(max_length=100, default="25-30 minutes", help_text="Expected delivery time")
    
    # Tax Settings
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0825, help_text="Tax rate (e.g., 0.0825 for 8.25%)")
    
    # Navigation Text
    nav_home_text = models.CharField(max_length=50, default="Home", help_text="Home navigation text")
    nav_menu_text = models.CharField(max_length=50, default="Menu", help_text="Menu navigation text")
    nav_about_text = models.CharField(max_length=50, default="About", help_text="About navigation text")
    nav_contact_text = models.CharField(max_length=50, default="Contact", help_text="Contact navigation text")
    nav_cart_text = models.CharField(max_length=50, default="Cart", help_text="Cart navigation text")
    
    # Footer Text
    footer_copyright = models.CharField(max_length=200, default="© 2024 Ramza's Chillas. All rights reserved.", help_text="Copyright text")
    footer_description = models.TextField(default="Serving the finest food with fresh ingredients and chill vibes since 2024. Your go-to spot for quality meals in a relaxed atmosphere.", help_text="Footer description")
    
    # Images
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Restaurant logo (recommended: 200x200px)")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Favicon (recommended: 32x32px)")
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f"{self.site_name} Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Only one SiteSettings instance is allowed')
        super().save(*args, **kwargs)
