from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Populate the database with sample categories and products'

    def handle(self, *args, **options):
        self.stdout.write('🥬 Populating Fresh Mart database...\n')

        # Create categories
        categories_data = [
            {'name': 'Fruits', 'slug': 'fruits', 'description': 'Fresh seasonal fruits from local farms'},
            {'name': 'Vegetables', 'slug': 'vegetables', 'description': 'Organic and fresh vegetables'},
            {'name': 'Dairy', 'slug': 'dairy', 'description': 'Farm-fresh dairy products'},
            {'name': 'Bakery', 'slug': 'bakery', 'description': 'Freshly baked goods daily'},
            {'name': 'Meat', 'slug': 'meat', 'description': 'Premium quality meat products'},
            {'name': 'Beverages', 'slug': 'beverages', 'description': 'Refreshing drinks and juices'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'  ✅ Created category: {category.name}')
            else:
                self.stdout.write(f'  ⏭️  Category already exists: {category.name}')

        # Create products
        products_data = [
            # Fruits
            {'name': 'Organic Apples', 'slug': 'organic-apples', 'category': 'Fruits', 'emoji': '🍎',
             'price': 4.99, 'old_price': 6.99, 'description': 'Crispy organic apples from local orchards.',
             'is_organic': True, 'is_featured': True, 'stock': 50},
            {'name': 'Fresh Bananas', 'slug': 'fresh-bananas', 'category': 'Fruits', 'emoji': '🍌',
             'price': 2.49, 'description': 'Ripe and sweet bananas, rich in potassium.',
             'is_featured': True, 'stock': 80},
            {'name': 'Juicy Oranges', 'slug': 'juicy-oranges', 'category': 'Fruits', 'emoji': '🍊',
             'price': 5.99, 'old_price': 7.49, 'description': 'Sun-ripened oranges perfect for juice.',
             'is_organic': True, 'stock': 60},
            {'name': 'Sweet Strawberries', 'slug': 'sweet-strawberries', 'category': 'Fruits', 'emoji': '🍓',
             'price': 6.99, 'description': 'Hand-picked sweet strawberries.',
             'is_featured': True, 'is_organic': True, 'stock': 30},
            
            # Vegetables
            {'name': 'Fresh Broccoli', 'slug': 'fresh-broccoli', 'category': 'Vegetables', 'emoji': '🥦',
             'price': 3.49, 'description': 'Crisp green broccoli heads.',
             'is_organic': True, 'is_featured': True, 'stock': 40},
            {'name': 'Organic Spinach', 'slug': 'organic-spinach', 'category': 'Vegetables', 'emoji': '🥬',
             'price': 2.99, 'description': 'Fresh organic spinach leaves.',
             'is_organic': True, 'stock': 50},
            {'name': 'Red Tomatoes', 'slug': 'red-tomatoes', 'category': 'Vegetables', 'emoji': '🍅',
             'price': 3.99, 'old_price': 4.99, 'description': 'Vine-ripened red tomatoes.',
             'is_featured': True, 'stock': 65},
            {'name': 'Sweet Carrots', 'slug': 'sweet-carrots', 'category': 'Vegetables', 'emoji': '🥕',
             'price': 2.49, 'description': 'Sweet and crunchy carrots.',
             'is_organic': True, 'stock': 70},
            
            # Dairy
            {'name': 'Fresh Whole Milk', 'slug': 'fresh-whole-milk', 'category': 'Dairy', 'emoji': '🥛',
             'price': 4.49, 'description': 'Farm-fresh whole milk, 1 gallon.',
             'is_featured': True, 'stock': 40},
            {'name': 'Organic Cheese', 'slug': 'organic-cheese', 'category': 'Dairy', 'emoji': '🧀',
             'price': 8.99, 'old_price': 10.99, 'description': 'Aged organic cheddar cheese.',
             'is_organic': True, 'stock': 25},
            
            # Bakery
            {'name': 'Whole Wheat Bread', 'slug': 'whole-wheat-bread', 'category': 'Bakery', 'emoji': '🍞',
             'price': 3.99, 'description': 'Freshly baked whole wheat bread.',
             'is_featured': True, 'stock': 20},
            {'name': 'Croissants Pack', 'slug': 'croissants-pack', 'category': 'Bakery', 'emoji': '🥐',
             'price': 5.99, 'old_price': 7.49, 'description': 'Buttery flaky croissants.',
             'stock': 15},
            
            # Meat
            {'name': 'Chicken Breast', 'slug': 'chicken-breast', 'category': 'Meat', 'emoji': '🍗',
             'price': 9.99, 'description': 'Boneless skinless chicken breast.',
             'is_featured': True, 'stock': 30},
            {'name': 'Ground Beef', 'slug': 'ground-beef', 'category': 'Meat', 'emoji': '🥩',
             'price': 11.99, 'old_price': 13.99, 'description': 'Premium lean ground beef.',
             'stock': 25},
            
            # Beverages
            {'name': 'Orange Juice', 'slug': 'orange-juice', 'category': 'Beverages', 'emoji': '🧃',
             'price': 4.99, 'description': 'Freshly squeezed orange juice.',
             'is_featured': True, 'stock': 40},
            {'name': 'Green Smoothie', 'slug': 'green-smoothie', 'category': 'Beverages', 'emoji': '🥤',
             'price': 6.49, 'description': 'Organic green smoothie blend.',
             'is_organic': True, 'stock': 20},
        ]

        for prod_data in products_data:
            category_name = prod_data.pop('category')
            
            # ✅ FIX: Use get_or_create so it never crashes if category is missing
            category_obj, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower()}
            )
            prod_data['category_fk'] = category_obj

            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'  ✅ Created product: {product.name}')
            else:
                self.stdout.write(f'  ⏭️  Product already exists: {product.name}')

        # Create test users
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@freshmart.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
            self.stdout.write('  ✅ Created test user: testuser / testpass123')

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@freshmart.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('  ✅ Created admin user: admin / admin123')

        self.stdout.write('\n🎉 Database populated successfully!')