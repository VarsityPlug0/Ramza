# Ramza's Chillas - Restaurant Management System

A comprehensive Django-based restaurant management system with full content management capabilities.

## Features

### Content Management System
- **Full Admin Control**: Admins can modify every text element on the site through the Django admin interface
- **Dynamic Content Sections**: Manage content for different sections of the website (home hero, menu hero, features, etc.)
- **Image Management**: Upload and manage all images used throughout the site
- **Site Settings**: Control global site settings like restaurant name, contact info, business hours, etc.

### Menu Management
- **Category Management**: Organize menu items into categories with images
- **Menu Items**: Add, edit, and manage menu items with pricing, descriptions, and images
- **Inventory Tracking**: Track stock levels with low stock alerts
- **Featured Items**: Highlight special items on the homepage

### Order Management
- **Cart System**: Shopping cart functionality with local storage
- **Order Processing**: Complete order processing workflow

## Content Management

### Admin Interface
The admin interface at `/admin/` provides complete control over all site content:

1. **Content Sections**: Manage text content for each section of the website
   - Home Hero Section
   - Home Features Section
   - Home Call to Action
   - Menu Hero Section
   - Footer Content
   - Navigation Content

2. **Site Images**: Upload and manage all images used on the site
   - Logo images
   - Hero images
   - Background images
   - Gallery images
   - Category images
   - Menu item images

3. **Site Settings**: Control global site settings
   - Restaurant name and description
   - Contact information
   - Business hours
   - Delivery settings
   - Navigation text
   - Footer content

### Dynamic Templates
All templates use dynamic content from the database:
- Home page content is fully customizable
- Menu page content is fully customizable
- Navigation and footer use dynamic site settings
- All text can be modified through the admin interface

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Populate default content: `python manage.py populate_content`
8. Run the development server: `python manage.py runserver`

## Management Commands

- `populate_content`: Creates default content sections and site settings
- `add_sample_images`: Adds sample images for demonstration

## Models

### ContentSection
Manages all text content on the website with fields for:
- Section type (home hero, menu hero, etc.)
- Title, subtitle, description
- Button text and URL
- Extra text fields for complex content
- Image and background image fields
- SEO settings

### SiteImage
Manages all images used throughout the site:
- Image types (logo, hero, background, gallery, etc.)
- Alt text for accessibility
- Sort order for display
- Association with content sections

### SiteSettings
Global site settings that control:
- Restaurant information
- Contact details
- Business hours
- Delivery settings
- Tax rates
- Navigation text
- Footer content

## Templates

All templates use the dynamic content from the database:
- `base.html`: Base template with dynamic navigation and footer
- `home.html`: Homepage with dynamic hero, features, and CTA sections
- `menu.html`: Menu page with dynamic hero section
- `cart.html`: Shopping cart page
- `checkout.html`: Checkout page

## Context Processors

The system uses context processors to make dynamic content available to all templates:
- `site_content`: Provides content sections, site settings, and site images
- `background_context`: Provides background images for non-home pages

## Media Handling

All uploaded images are stored in the `media/` directory with proper URL handling to ensure images display correctly both in the admin interface and on the frontend.

## Customization

Admins can fully customize:
- All text content on every page
- All images used throughout the site
- Site-wide settings like business hours and contact info
- Menu items, categories, and pricing
- Featured items and special offers

## Deployment

For production deployment, make sure to:
1. Set `DEBUG = False` in settings.py
2. Set a secure `SECRET_KEY`
3. Configure allowed hosts
4. Set up a proper database (PostgreSQL recommended)
5. Configure static and media file serving
6. Set up a web server (Nginx/Apache) with WSGI (Gunicorn/uWSGI)

## Currency

All prices are displayed in South African Rand (R).

## Version Control

- Static files are included in version control
- Media files (uploaded by users) are excluded from version control
- Database files are excluded from version control