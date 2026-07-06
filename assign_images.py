import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fit_and_fine.settings')
django.setup()

from catalogue.models import Product

# Assign images based on category or name
for product in Product.objects.all():
    if "Diet Plan" in product.name:
        product.image_url = "/media/products/diet_plan.png"
    elif "Sattu" in product.name:
        product.image_url = "/media/products/sattu_mix.png"
    elif "Gut Health" in product.name:
        product.image_url = "/media/products/gut_drink.png"
    else:
        # Default to tea for the rest
        product.image_url = "/media/products/slimming_tea.png"
    product.save()

print("Images assigned successfully!")
