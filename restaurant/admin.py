from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, MenuItem, SiteSettings, ContentSection, SiteImage
from django.db import models
from django.forms import Textarea

# Custom Admin Site Header
admin.site.site_header = "Ramza's Chillas Admin"
admin.site.site_title = "Restaurant Management"
admin.site.index_title = "Welcome to Restaurant Admin Dashboard"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_count', 'is_active', 'sort_order', 'image_preview', 'created_at')
    list_editable = ('is_active', 'sort_order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('sort_order', 'name')
    
    fieldsets = (
        ('🏷️ Basic Information', {
            'fields': ('name', 'description'),
            'description': 'Enter the category name and a brief description.'
        }),
        ('🖼️ Visual Settings', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a category image (recommended size: 400x300px). This image will be displayed on the homepage category grid.'
        }),
        ('⚙️ Display Settings', {
            'fields': ('is_active', 'sort_order'),
            'description': 'Control when and how this category appears on your menu. Lower sort order numbers appear first.'
        }),
    )
    
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "No image uploaded"
    image_preview.short_description = 'Current Image'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['description'].widget = Textarea(attrs={'rows': 3})
        return form

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_status', 'is_available', 'is_featured', 'image_preview', 'updated_at')
    list_editable = ('price', 'is_available', 'is_featured')
    list_filter = ('category', 'is_available', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'ingredients')
    ordering = ('category', 'name')
    
    fieldsets = (
        ('🍔 Item Details', {
            'fields': ('name', 'description', 'category'),
            'description': 'Basic information about this menu item. The description will be shown to customers.'
        }),
        ('💰 Pricing', {
            'fields': ('price',),
            'description': 'Set the price customers will pay for this item.'
        }),
        ('🖼️ Images', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a high-quality food photo (recommended size: 600x400px). This is crucial for attracting customers!'
        }),
        ('📦 Inventory Management', {
            'fields': ('stock_quantity', 'low_stock_threshold'),
            'description': 'Track how many items you have in stock. You will be alerted when stock runs low.'
        }),
        ('🔧 Additional Info', {
            'fields': ('ingredients', 'preparation_time', 'calories'),
            'description': 'Optional details that help with kitchen operations and customer information.'
        }),
        ('👁️ Visibility Settings', {
            'fields': ('is_available', 'is_featured'),
            'description': 'Control where this item appears: Available = shows on menu, Featured = shows on homepage.'
        }),
    )
    
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="120" height="80" style="border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "⚠️ No image uploaded - Upload an image to make this item more appealing!"
    image_preview.short_description = 'Food Photo'
    
    def stock_status(self, obj):
        if obj.stock_quantity <= 0:
            return format_html('<span style="color: red; font-weight: bold;">❌ OUT OF STOCK</span>')
        elif obj.stock_quantity <= obj.low_stock_threshold:
            return format_html('<span style="color: orange; font-weight: bold;">⚠️ LOW STOCK ({})</span>', obj.stock_quantity)
        else:
            return format_html('<span style="color: green;">✅ In Stock ({})</span>', obj.stock_quantity)
    stock_status.short_description = 'Stock Status'
    
    actions = ['mark_as_featured', 'remove_from_featured', 'mark_as_unavailable', 'mark_as_available']
    
    def mark_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} items marked as featured and will appear on homepage.')
    mark_as_featured.short_description = '⭐ Mark selected items as featured'
    
    def remove_from_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} items removed from featured section.')
    remove_from_featured.short_description = '📤 Remove from featured'
    
    def mark_as_unavailable(self, request, queryset):
        count = queryset.update(is_available=False)
        self.message_user(request, f'{count} items marked as unavailable and hidden from menu.')
    mark_as_unavailable.short_description = '🚫 Mark as unavailable'
    
    def mark_as_available(self, request, queryset):
        count = queryset.update(is_available=True)
        self.message_user(request, f'{count} items marked as available and visible on menu.')
    mark_as_available.short_description = '✅ Mark as available'

@admin.register(ContentSection)
class ContentSectionAdmin(admin.ModelAdmin):
    list_display = ('section', 'title', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    list_filter = ('section', 'is_active')
    search_fields = ('title', 'subtitle', 'description')
    ordering = ('section',)
    
    fieldsets = (
        ('📍 Section Information', {
            'fields': ('section',),
            'description': 'Select which part of the website this content is for.'
        }),
        ('📝 Main Content', {
            'fields': ('title', 'subtitle', 'description'),
            'description': 'The main text content that will appear on your website.'
        }),
        ('🔗 Action Button', {
            'fields': ('button_text', 'button_url'),
            'description': 'Optional: Add a button with custom text and link.'
        }),
        ('📝 Additional Text Fields', {
            'fields': ('extra_text_1', 'extra_text_2', 'extra_text_3'),
            'description': 'Extra text fields for complex sections. Use as needed.',
            'classes': ('collapse',)
        }),
        ('🖼️ Images', {
            'fields': ('image', 'background_image', 'image_preview'),
            'description': 'Upload images for this section.'
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'description': 'Search engine optimization settings.',
            'classes': ('collapse',)
        }),
        ('⚙️ Settings', {
            'fields': ('is_active',),
            'description': 'Control whether this section is displayed.'
        }),
    )
    
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        html = ""
        if obj.image:
            html += format_html('<div><strong>Main Image:</strong><br><img src="{}" width="200" style="border-radius: 8px; margin: 5px 0;" /></div>', obj.image.url)
        if obj.background_image:
            html += format_html('<div><strong>Background Image:</strong><br><img src="{}" width="200" style="border-radius: 8px; margin: 5px 0;" /></div>', obj.background_image.url)
        return html if html else "No images uploaded"
    image_preview.short_description = 'Image Preview'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make text areas larger
        form.base_fields['description'].widget = Textarea(attrs={'rows': 4})
        form.base_fields['extra_text_1'].widget = Textarea(attrs={'rows': 3})
        form.base_fields['extra_text_2'].widget = Textarea(attrs={'rows': 3})
        form.base_fields['extra_text_3'].widget = Textarea(attrs={'rows': 3})
        return form

@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_type', 'image_preview', 'file_size_display', 'is_active', 'sort_order', 'updated_at')
    list_editable = ('is_active', 'sort_order')
    list_filter = ('image_type', 'is_active', 'created_at')
    search_fields = ('name', 'alt_text', 'description')
    ordering = ('image_type', 'sort_order', 'name')
    filter_horizontal = ('used_in_sections',)
    
    fieldsets = (
        ('📋 Image Information', {
            'fields': ('name', 'image_type', 'description'),
            'description': 'Basic information about this image.'
        }),
        ('🖼️ Image File', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload your image file.'
        }),
        ('♿ Accessibility', {
            'fields': ('alt_text',),
            'description': 'Alt text for screen readers and accessibility.'
        }),
        ('🔗 Usage', {
            'fields': ('used_in_sections',),
            'description': 'Select which content sections use this image.'
        }),
        ('⚙️ Settings', {
            'fields': ('is_active', 'sort_order'),
            'description': 'Display settings and ordering.'
        }),
    )
    
    readonly_fields = ('image_preview', 'file_size_display')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "No image uploaded"
    image_preview.short_description = 'Preview'
    
    def file_size_display(self, obj):
        if obj.file_size_mb:
            return f"{obj.file_size_mb} MB"
        return "Unknown"
    file_size_display.short_description = 'File Size'
    
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def mark_as_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} images marked as active.')
    mark_as_active.short_description = '✅ Mark as active'
    
    def mark_as_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} images marked as inactive.')
    mark_as_inactive.short_description = '❌ Mark as inactive'
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    
    fieldsets = (
        ('🏪 Restaurant Information', {
            'fields': ('site_name', 'site_description'),
            'description': 'Your restaurant name and tagline as they appear on the website.'
        }),
        ('📞 Contact Information', {
            'fields': ('phone_number', 'email', 'address'),
            'description': 'How customers can reach you. This information appears in the footer and contact sections.'
        }),
        ('🕐 Business Hours', {
            'fields': ('opening_time', 'closing_time'),
            'description': 'When your restaurant is open for orders.'
        }),
        ('🚚 Delivery Settings', {
            'fields': ('delivery_fee', 'free_delivery_minimum', 'delivery_radius'),
            'description': 'Configure delivery pricing and coverage area.'
        }),
        ('💰 Tax Settings', {
            'fields': ('tax_rate',),
            'description': 'Local tax rate (e.g., 0.0825 for 8.25% tax).'
        }),
        ('🖼️ Site Images', {
            'fields': ('hero_image', 'logo', 'hero_preview', 'logo_preview'),
            'description': 'Upload your restaurant logo and hero image. These appear prominently on your website.'
        }),
    )
    
    readonly_fields = ('hero_preview', 'logo_preview')
    
    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" width="200" height="100" style="border-radius: 8px; object-fit: cover;" />', obj.hero_image.url)
        return "No hero image uploaded"
    hero_preview.short_description = 'Hero Image Preview'
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 8px; object-fit: cover;" />', obj.logo.url)
        return "No logo uploaded"
    logo_preview.short_description = 'Logo Preview'
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False

# Add some helpful text to the admin index
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_message'] = """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h2 style="margin: 0 0 10px 0;">🍔 Welcome to Ramza's Chillas Admin!</h2>
            <p style="margin: 0; opacity: 0.9;">Here's how to manage your restaurant:</p>
            <ul style="margin: 10px 0 0 20px; opacity: 0.9;">
                <li><strong>Menu Items:</strong> Add/edit food items, upload images, manage prices and stock</li>
                <li><strong>Categories:</strong> Organize your menu (Burgers, Pizzas, etc.)</li>
                <li><strong>Orders:</strong> View and manage customer orders, update status</li>
                <li><strong>Site Settings:</strong> Update restaurant info, delivery settings, and images</li>
            </ul>
        </div>
        """
        return super().index(request, extra_context)

# Replace the default admin site
admin_site = CustomAdminSite(name='custom_admin')
