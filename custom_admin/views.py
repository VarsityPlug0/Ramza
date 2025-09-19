from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from restaurant.models import MenuItem, Category, SiteSettings
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
from pathlib import Path

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_required(view_func):
    """Decorator to require admin authentication for all admin views"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('custom_admin:login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Admin Login View
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions')
    
    return render(request, 'custom_admin/login.html')

# Admin Logout
def admin_logout(request):
    logout(request)
    return redirect('custom_admin:login')

# Dashboard
@admin_required
def dashboard(request):
    # Get statistics
    total_items = MenuItem.objects.count()
    total_categories = Category.objects.filter(is_active=True).count()
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True).count()
    low_stock_items = MenuItem.objects.filter(stock_quantity__lte=5, is_available=True).count()
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Get website images for image gallery
    website_images = get_website_images()
    
    # Get background images
    background_images = get_background_images()
    
    context = {
        'total_items': total_items,
        'total_categories': total_categories,
        'featured_items': featured_items,
        'low_stock_items': low_stock_items,
        'recent_orders': recent_orders,
        'website_images': website_images,
        'background_images': background_images,
    }
    return render(request, 'custom_admin/dashboard.html', context)

def get_website_images():
    """Get all images currently used on the website"""
    images = {
        'menu_items': [],
        'categories': [],
        'site_settings': [],
        'static_images': [],
    }
    
    try:
        # Menu item images
        menu_items_with_images = MenuItem.objects.filter(image__isnull=False).exclude(image='')
        for item in menu_items_with_images:
            if item.image:
                images['menu_items'].append({
                    'name': item.name,
                    'image_url': item.image.url,
                    'type': 'Menu Item',
                    'status': 'Active' if item.is_available else 'Inactive',
                    'featured': item.is_featured,
                    'category': item.category.name if item.category else 'No Category'
                })
        
        # Category images
        categories_with_images = Category.objects.filter(image__isnull=False).exclude(image='')
        for category in categories_with_images:
            if category.image:
                images['categories'].append({
                    'name': category.name,
                    'image_url': category.image.url,
                    'type': 'Category',
                    'status': 'Active' if category.is_active else 'Inactive',
                    'sort_order': category.sort_order
                })
        
        # Site settings images
        try:
            site_settings = SiteSettings.objects.first()
            if site_settings:
                if site_settings.logo:
                    images['site_settings'].append({
                        'name': 'Restaurant Logo',
                        'image_url': site_settings.logo.url,
                        'type': 'Site Logo',
                        'status': 'Active'
                    })
                if site_settings.hero_image:
                    images['site_settings'].append({
                        'name': 'Hero Image',
                        'image_url': site_settings.hero_image.url,
                        'type': 'Hero Image',
                        'status': 'Active'
                    })
        except:
            pass
        
        # Static images from food folder
        static_folder = os.path.join(settings.BASE_DIR, 'static', 'images')
        if os.path.exists(static_folder):
            for filename in os.listdir(static_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    images['static_images'].append({
                        'name': filename,
                        'image_url': f'/static/images/{filename}',
                        'type': 'Static Image',
                        'status': 'Available'
                    })
    
    except Exception as e:
        # If there's any error, return empty structure
        pass
    
    return images

def get_background_images():
    """Get all background images available for the website"""
    background_images = {
        'images': [],
        'total_count': 0,
        'folder_path': '/static/images/background/',
        'status': 'active'
    }
    
    try:
        background_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'background')
        
        if os.path.exists(background_path):
            background_files = []
            
            for filename in os.listdir(background_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    file_path = os.path.join(background_path, filename)
                    file_size = os.path.getsize(file_path)
                    
                    background_files.append({
                        'name': filename,
                        'display_name': filename.replace('-', ' ').replace('_', ' ').title(),
                        'image_url': f'/static/images/background/{filename}',
                        'file_size': round(file_size / 1024, 1),  # Size in KB
                        'type': 'Background Image',
                        'status': 'Active',
                        'extension': filename.split('.')[-1].upper(),
                        'added_date': 'Unknown'  # Could be enhanced with file modification time
                    })
            
            background_images['images'] = sorted(background_files, key=lambda x: x['name'])
            background_images['total_count'] = len(background_files)
            
            if len(background_files) == 0:
                background_images['status'] = 'empty'
        else:
            background_images['status'] = 'folder_missing'
    
    except Exception as e:
        background_images['status'] = 'error'
        background_images['error_message'] = str(e)
    
    return background_images

# Menu Items Management
@admin_required
def menu_items(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    items = MenuItem.objects.all()
    
    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    if category_filter:
        items = items.filter(category_id=category_filter)
    
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'custom_admin/menu_items.html', context)

# Add/Edit Menu Item
@user_passes_test(is_admin)
def edit_menu_item(request, item_id=None):
    item = get_object_or_404(MenuItem, id=item_id) if item_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity', 0)
        is_available = request.POST.get('is_available') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        
        if item:
            item.name = name
            item.description = description
            item.price = price
            item.category_id = category_id
            item.stock_quantity = stock_quantity
            item.is_available = is_available
            item.is_featured = is_featured
            if request.FILES.get('image'):
                item.image = request.FILES['image']
            item.save()
            messages.success(request, 'Menu item updated successfully!')
        else:
            item = MenuItem.objects.create(
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                stock_quantity=stock_quantity,
                is_available=is_available,
                is_featured=is_featured,
                image=request.FILES.get('image')
            )
            messages.success(request, 'Menu item created successfully!')
        
        return redirect('custom_admin:menu_items')
    
    categories = Category.objects.filter(is_active=True)
    context = {
        'item': item,
        'categories': categories,
    }
    return render(request, 'custom_admin/edit_menu_item.html', context)

# Delete Menu Item
@user_passes_test(is_admin)
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('custom_admin:menu_items')

# Categories Management
@user_passes_test(is_admin)
def categories(request):
    categories = Category.objects.all().order_by('sort_order', 'name')
    context = {'categories': categories}
    return render(request, 'custom_admin/categories.html', context)

# Add/Edit Category
@user_passes_test(is_admin)
def edit_category(request, category_id=None):
    category = get_object_or_404(Category, id=category_id) if category_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        sort_order = request.POST.get('sort_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        if category:
            category.name = name
            category.description = description
            category.sort_order = sort_order
            category.is_active = is_active
            if request.FILES.get('image'):
                category.image = request.FILES['image']
            category.save()
            messages.success(request, 'Category updated successfully!')
        else:
            category = Category.objects.create(
                name=name,
                description=description,
                sort_order=sort_order,
                is_active=is_active,
                image=request.FILES.get('image')
            )
            messages.success(request, 'Category created successfully!')
        
        return redirect('custom_admin:categories')
    
    context = {'category': category}
    return render(request, 'custom_admin/edit_category.html', context)

# Orders Management
@user_passes_test(is_admin)
def orders(request):
    status_filter = request.GET.get('status', '')
    
    orders = Order.objects.all().order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'custom_admin/orders.html', context)

# Update Order Status
@csrf_exempt
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'success': False})

# Site Settings
@user_passes_test(is_admin)
def site_settings(request):
    settings, created = SiteSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        settings.site_name = request.POST.get('site_name', '')
        settings.site_description = request.POST.get('site_description', '')
        settings.phone_number = request.POST.get('phone_number', '')
        settings.email = request.POST.get('email', '')
        settings.address = request.POST.get('address', '')
        settings.delivery_fee = request.POST.get('delivery_fee', 0)
        
        if request.FILES.get('logo'):
            settings.logo = request.FILES['logo']
        if request.FILES.get('hero_image'):
            settings.hero_image = request.FILES['hero_image']
        
        settings.save()
        messages.success(request, 'Site settings updated successfully!')
        return redirect('custom_admin:site_settings')
    
    context = {'settings': settings}
    return render(request, 'custom_admin/site_settings.html', context)