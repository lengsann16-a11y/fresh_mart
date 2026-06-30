"""
Optional: Download placeholder images for products.
Requires: pip install requests
Usage: python manage.py download_images
"""

import os
import urllib.request
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Download placeholder images for products'

    def handle(self, *args, **options):
        images_dir = os.path.join(settings.BASE_DIR, 'store', 'static', 'images', 'products')
        os.makedirs(images_dir, exist_ok=True)

        # Free placeholder images (from placeholder.com)
        products = [
            ('apples.jpg', 'https://via.placeholder.com/400x300/27ae60/ffffff?text=Apples'),
            ('bananas.jpg', 'https://via.placeholder.com/400x300/f1c40f/ffffff?text=Bananas'),
            ('oranges.jpg', 'https://via.placeholder.com/400x300/e67e22/ffffff?text=Oranges'),
            ('strawberries.jpg', 'https://via.placeholder.com/400x300/e74c3c/ffffff?text=Strawberries'),
            ('broccoli.jpg', 'https://via.placeholder.com/400x300/2ecc71/ffffff?text=Broccoli'),
            ('tomatoes.jpg', 'https://via.placeholder.com/400x300/c0392b/ffffff?text=Tomatoes'),
            ('milk.jpg', 'https://via.placeholder.com/400x300/ecf0f1/333333?text=Milk'),
            ('bread.jpg', 'https://via.placeholder.com/400x300/d4a574/ffffff?text=Bread'),
            ('chicken.jpg', 'https://via.placeholder.com/400x300/e8ae68/ffffff?text=Chicken'),
            ('juice.jpg', 'https://via.placeholder.com/400x300/f39c12/ffffff?text=Orange+Juice'),
        ]

        for filename, url in products:
            filepath = os.path.join(images_dir, filename)
            if not os.path.exists(filepath):
                try:
                    urllib.request.urlretrieve(url, filepath)
                    self.stdout.write(f'  ✅ Downloaded: {filename}')
                except Exception as e:
                    self.stdout.write(f'  ❌ Failed: {filename} - {e}')
            else:
                self.stdout.write(f'  ⏭️  Already exists: {filename}')

        self.stdout.write('\n✅ Done! Images saved to store/static/images/products/')