from django.core.management.base import BaseCommand
from restaurant.models import SiteImage
import os

class Command(BaseCommand):
    help = 'Add sample images to demonstrate the image management system'

    def handle(self, *args, **options):
        # Create sample images
        sample_images = [
            {
                'name': 'Logo Image',
                'image_type': 'logo',
                'alt_text': 'Ramza\'s Chillas Logo',
                'description': 'Main logo for the restaurant',
                'sort_order': 1,
            },
            {
                'name': 'Hero Image 1',
                'image_type': 'hero',
                'alt_text': 'Delicious food presentation',
                'description': 'Featured hero image for homepage',
                'sort_order': 1,
            },
            {
                'name': 'Hero Image 2',
                'image_type': 'hero',
                'alt_text': 'Restaurant interior',
                'description': 'Interior view of the restaurant',
                'sort_order': 2,
            },
            {
                'name': 'Background Pattern',
                'image_type': 'background',
                'alt_text': 'Subtle background pattern',
                'description': 'Background pattern for website',
                'sort_order': 1,
            },
            {
                'name': 'Gallery Image 1',
                'image_type': 'gallery',
                'alt_text': 'Customers enjoying food',
                'description': 'Happy customers enjoying our food',
                'sort_order': 1,
            },
            {
                'name': 'Gallery Image 2',
                'image_type': 'gallery',
                'alt_text': 'Chef preparing food',
                'description': 'Our chef preparing delicious meals',
                'sort_order': 2,
            },
        ]

        created_count = 0
        for image_data in sample_images:
            # Check if image already exists
            if not SiteImage.objects.filter(name=image_data['name']).exists():
                image = SiteImage.objects.create(**image_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created image: {image.name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Image already exists: {image_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {created_count} sample images!')
        )