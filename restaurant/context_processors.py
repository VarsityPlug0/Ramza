import os
import random
from django.conf import settings
from .models import SiteSettings, ContentSection, SiteImage
import logging

logger = logging.getLogger(__name__)

def background_context(request):
    """
    Context processor to add background images to templates.
    Only applies to non-home and non-admin pages.
    """
    # Check if this is a home page or admin page
    path = request.path
    
    # Debug logging
    logger.info(f"Background context called for path: {path}")
    
    # Skip background for home page and admin pages
    if path == '/' or path.startswith('/dashboard/') or path.startswith('/admin/'):
        logger.info(f"Skipping background for path: {path}")
        return {}
    
    # Get random background image or gradient
    background_image = get_random_background()
    gradient_class = get_random_gradient_class()
    logger.info(f"Background image selected: {background_image}, Gradient class: {gradient_class}")
    
    return {
        'page_background': background_image,
        'gradient_class': gradient_class,
        'has_background': True,
    }

def get_random_gradient_class():
    """Get a random gradient class when no background images are available"""
    gradient_classes = ['gradient-1', 'gradient-2', 'gradient-3', 'gradient-4']
    return random.choice(gradient_classes)

def get_random_background():
    """Get a random background image from the background folder"""
    try:
        background_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'background')
        logger.info(f"Looking for background images in: {background_path}")
        
        if os.path.exists(background_path):
            background_files = [f for f in os.listdir(background_path) 
                              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
                              and not f.startswith('.')]
            logger.info(f"Found background files: {background_files}")
            
            if background_files:
                selected_file = random.choice(background_files)
                logger.info(f"Selected background file: {selected_file}")
                return f'images/background/{selected_file}'
            else:
                logger.warning("No background image files found")
        else:
            logger.error(f"Background path does not exist: {background_path}")
    except Exception as e:
        logger.error(f"Error in get_random_background: {e}")
    
    # Fallback to a subtle default background if no images found
    logger.info("Returning None - no background image available")
    return None

def site_content(request):
    """Add dynamic site content to all templates"""
    context = {}
    
    # Get site settings
    try:
        site_settings = SiteSettings.objects.first()
        if site_settings:
            context['site_settings'] = site_settings
    except Exception as e:
        logger.warning(f"Could not fetch site settings: {e}")
        # Provide defaults
        context['site_settings'] = None
    
    # Get content sections
    try:
        content_sections = {}
        sections = ContentSection.objects.filter(is_active=True)
        for section in sections:
            content_sections[section.section] = section
        context['content_sections'] = content_sections
    except Exception as e:
        logger.warning(f"Could not fetch content sections: {e}")
        context['content_sections'] = {}
    
    # Get site images by type
    try:
        site_images = {}
        images = SiteImage.objects.filter(is_active=True).order_by('sort_order')
        for image in images:
            if image.image_type not in site_images:
                site_images[image.image_type] = []
            site_images[image.image_type].append(image)
        context['site_images'] = site_images
    except Exception as e:
        logger.warning(f"Could not fetch site images: {e}")
        context['site_images'] = {}
    
    return context