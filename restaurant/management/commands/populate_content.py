from django.core.management.base import BaseCommand
from restaurant.models import SiteSettings, ContentSection
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate default content sections and site settings'

    def handle(self, *args, **options):
        # Create or update SiteSettings
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': "Ramza's Chillas",
                'site_description': "Chill Vibes • Hot Food",
                'phone_number': "(555) 123-CHILL",
                'email': "hello@ramzaschillas.com",
                'address': "123 Chill Street, Island City",
                'facebook_url': "https://facebook.com/ramzaschillas",
                'instagram_url': "https://instagram.com/ramzaschillas",
                'twitter_url': "https://twitter.com/ramzaschillas",
                'opening_time': "09:00",
                'closing_time': "22:00",
                'business_hours_text': "Mon-Thu: 11:00 AM - 10:00 PM\\nFri-Sat: 11:00 AM - 11:00 PM\\nSunday: 12:00 PM - 9:00 PM",
                'delivery_fee': "3.99",
                'free_delivery_minimum': "25.00",
                'delivery_radius': 5,
                'delivery_time_text': "25-30 minutes",
                'tax_rate': "0.0825",
                'nav_home_text': "Home",
                'nav_menu_text': "Menu",
                'nav_about_text': "About",
                'nav_contact_text': "Contact",
                'nav_cart_text': "Cart",
                'footer_copyright': "© 2024 Ramza's Chillas. All rights reserved.",
                'footer_description': "Serving the finest food with fresh ingredients and chill vibes since 2024. Your go-to spot for quality meals in a relaxed atmosphere.",
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created SiteSettings')
            )
        else:
            self.stdout.write(
                self.style.WARNING('SiteSettings already exists')
            )

        # Create default content sections
        content_sections = [
            {
                'section': 'home_hero',
                'title': 'Chill Vibes & Hot Chillas',
                'subtitle': 'Experience the ultimate chill spot with the hottest food in town. Fresh ingredients, cool atmosphere, amazing taste.',
                'button_text': 'Order Now',
                'button_url': '/menu/',
            },
            {
                'section': 'home_features',
                'title': 'Why Choose Ramza\'s Chillas?',
                'description': 'Chill atmosphere, hot food, cool service - we\'re committed to providing you with the best experience through quality, speed, and unmatched vibes.',
            },
            {
                'section': 'home_cta',
                'title': 'Ready to Chill & Eat?',
                'subtitle': 'Browse our full menu and place your order for delivery or pickup. Let\'s get this chill session started!',
                'button_text': 'View Full Menu',
                'button_url': '/menu/',
            },
            {
                'section': 'menu_hero',
                'title': 'Our Chill Menu',
                'subtitle': 'Discover our signature chillas, crafted with the finest ingredients and served with unmatched flavor',
                'description': 'Fresh • Hot • Delicious',
            },
            {
                'section': 'footer',
                'title': 'Ramza\'s Chillas',
                'subtitle': 'Chill Vibes • Hot Food',
            },
            {
                'section': 'navigation',
                'title': 'Ramza\'s Chillas',
                'subtitle': 'Chill Vibes • Hot Food',
            },
        ]

        for section_data in content_sections:
            section, created = ContentSection.objects.get_or_create(
                section=section_data['section'],
                defaults=section_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created content section: {section_data["section"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Content section already exists: {section_data["section"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated default content!')
        )