from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import random
import os
from django.conf import settings
from .models import Category, MenuItem, SiteSettings, ContentSection, SiteImage

# Fallback food images
FOOD_IMAGES = [
    'images/Pork Rib Kota.jpeg',
    'images/download (1).jpeg',
    'images/download (2).jpeg', 
    'images/download (3).jpeg',
    'images/download.jpeg',
    'images/f7e6fd36-3419-4899-9bae-5bb98585a7aa.jpg',
    'images/image.jpg',
    'images/insta _ @gorgeous_thato_ (1).jpeg',
    'images/insta _ @gorgeous_thato_.jpeg'
]

def get_random_background():
    """Get a random background image from the background folder"""
    try:
        background_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'background')
        if os.path.exists(background_path):
            background_files = [f for f in os.listdir(background_path) 
                              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
            if background_files:
                return f'images/background/{random.choice(background_files)}'
    except Exception:
        pass
    
    # Fallback to a food image if no background images found
    return random.choice(FOOD_IMAGES)

def home(request):
    try:
        # Get data from database
        categories = Category.objects.filter(is_active=True)[:4]
        featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:3]
        
        # If no featured items, get some random available items
        if not featured_items:
            featured_items = MenuItem.objects.filter(is_available=True)[:3]
            
        # Convert to list and add fallback images
        categories_list = []
        for i, cat in enumerate(categories):
            categories_list.append({
                'name': cat.name,
                'description': cat.description,
                'image': cat.image.url if cat.image else random.choice(FOOD_IMAGES)
            })
            
        # Ensure we have at least 4 categories for the template
        while len(categories_list) < 4:
            default_categories = [
                {'name': 'Burgers', 'description': 'Juicy burgers', 'image': random.choice(FOOD_IMAGES)},
                {'name': 'Pizzas', 'description': 'Wood-fired pizzas', 'image': random.choice(FOOD_IMAGES)},
                {'name': 'Drinks', 'description': 'Refreshing beverages', 'image': random.choice(FOOD_IMAGES)},
                {'name': 'Sides', 'description': 'Perfect sides', 'image': random.choice(FOOD_IMAGES)},
            ]
            if len(categories_list) < len(default_categories):
                categories_list.append(default_categories[len(categories_list)])
            else:
                break
                
        featured_list = []
        for item in featured_items:
            featured_list.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'image': item.image.url if item.image else random.choice(FOOD_IMAGES)
            })
            
        # Ensure we have at least 3 featured items
        while len(featured_list) < 3:
            default_featured = [
                {'name': 'Chill Burger', 'price': 12.99, 'image': random.choice(FOOD_IMAGES)},
                {'name': 'Chilla Margherita', 'price': 18.99, 'image': random.choice(FOOD_IMAGES)},
                {'name': 'Ramza Fries', 'price': 4.99, 'image': random.choice(FOOD_IMAGES)},
            ]
            if len(featured_list) < len(default_featured):
                featured_list.append(default_featured[len(featured_list)])
            else:
                break
            
    except Exception as e:
        # Fallback data if database has issues
        categories_list = [
            {'name': 'Burgers', 'description': 'Juicy burgers', 'image': random.choice(FOOD_IMAGES)},
            {'name': 'Pizzas', 'description': 'Wood-fired pizzas', 'image': random.choice(FOOD_IMAGES)},
            {'name': 'Drinks', 'description': 'Refreshing beverages', 'image': random.choice(FOOD_IMAGES)},
            {'name': 'Sides', 'description': 'Perfect sides', 'image': random.choice(FOOD_IMAGES)},
        ]
        featured_list = [
            {'name': 'Chill Burger', 'price': 12.99, 'image': random.choice(FOOD_IMAGES)},
            {'name': 'Chilla Margherita', 'price': 18.99, 'image': random.choice(FOOD_IMAGES)},
            {'name': 'Ramza Fries', 'price': 4.99, 'image': random.choice(FOOD_IMAGES)},
        ]
    
    context = {
        'featured_items': featured_list,
        'categories': categories_list,
    }
    return render(request, 'home.html', context)

def menu(request):
    try:
        # Get all available menu items from database
        menu_items = MenuItem.objects.filter(is_available=True).select_related('category')
        categories = ['All'] + list(Category.objects.filter(is_active=True).values_list('name', flat=True))
        
        # Convert queryset to list with proper image handling
        menu_items_list = []
        for item in menu_items:
            menu_items_list.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'category': item.category.name,
                'image': item.image.url if item.image else None  # Changed this to None instead of random image
            })
        
        # If no items exist, create fallback data
        if not menu_items_list:
            # Create categories first
            burger_cat, _ = Category.objects.get_or_create(name='Burgers', defaults={'sort_order': 1})
            pizza_cat, _ = Category.objects.get_or_create(name='Pizzas', defaults={'sort_order': 2})
            drinks_cat, _ = Category.objects.get_or_create(name='Drinks', defaults={'sort_order': 3})
            sides_cat, _ = Category.objects.get_or_create(name='Sides', defaults={'sort_order': 4})
            
            # Create sample menu items
            MenuItem.objects.get_or_create(
                name='Chill Burger',
                defaults={
                    'description': 'Laid-back beef patty with fresh chilled ingredients',
                    'price': 12.99,
                    'category': burger_cat,
                    'is_featured': True
                }
            )
            MenuItem.objects.get_or_create(
                name='Ramza Special',
                defaults={
                    'description': 'Signature chicken with avocado and cool ranch',
                    'price': 14.99,
                    'category': burger_cat
                }
            )
            MenuItem.objects.get_or_create(
                name='Chilla Margherita',
                defaults={
                    'description': 'Classic pizza with our signature chill twist',
                    'price': 18.99,
                    'category': pizza_cat,
                    'is_featured': True
                }
            )
            MenuItem.objects.get_or_create(
                name='Fire Pepperoni',
                defaults={
                    'description': 'Hot pepperoni with cool mozzarella balance',
                    'price': 22.99,
                    'category': pizza_cat
                }
            )
            MenuItem.objects.get_or_create(
                name='Chill Cola',
                defaults={
                    'description': 'Ice-cold refreshing cola to keep you cool',
                    'price': 2.99,
                    'category': drinks_cat
                }
            )
            MenuItem.objects.get_or_create(
                name='Ramza Fries',
                defaults={
                    'description': 'Golden fries with our special chill seasoning',
                    'price': 4.99,
                    'category': sides_cat,
                    'is_featured': True
                }
            )
            
            # Reload data
            menu_items = MenuItem.objects.filter(is_available=True).select_related('category')
            categories = ['All'] + list(Category.objects.filter(is_active=True).values_list('name', flat=True))
            
    except Exception as e:
        # Fallback data
        menu_items = []
        categories = ['All', 'Burgers', 'Pizzas', 'Drinks', 'Sides']
    
    context = {
        'menu_items': menu_items_list if 'menu_items_list' in locals() else [],
        'categories': categories,
    }
    return render(request, 'menu.html', context)

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')