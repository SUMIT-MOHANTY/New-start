import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fit_and_fine.settings')
django.setup()

from catalogue.models import Category, Product

def seed():
    # Clear existing data
    Category.objects.all().delete()
    
    # Create Categories
    tea_cat = Category.objects.create(name='Wellness Teas', description='100% Natural ingredients. Zero side effects. Plastic free tea bags.')
    diet_cat = Category.objects.create(name='Diet Plans', description='Personalized diet plans for various health goals.')
    protein_cat = Category.objects.create(name='Plant Based Protein', description='Best Plant based Protein Sattu Pre-Mix.')
    drink_cat = Category.objects.create(name='Health Drinks', description='Drinks to boost your health and immunity.')

    # Diet Plans
    Product.objects.create(
        category=diet_cat,
        name='45 Days Personalized Diet Plan',
        description='Get your best health ever. Obesity, Weight gain, Diabetes, Pregnancy, Hypertension, Thyroid, PCOD/PCOS, Pre wedding diet plan, Skin & Hair, Lifestyle guidance, Recipes guidance, Daily follow up, Workout guidance, Healthy tips.',
        price=None, offer_price=700, weight='45 Days',
        benefits='Weight management, Disease management'
    )

    # Teas
    Product.objects.create(
        category=tea_cat,
        name='Slimming Tea - Fat To Fab',
        description='Boosts Metabolism, Reduce Sugar Cravings, Improve Digestion, Weight Management, Liver Protection, Control Cholesterol.',
        price=499, offer_price=399, weight='30 Tea Bags',
        benefits='Boosts Metabolism,Reduce Sugar Cravings,Improve Digestion,Weight Management,Liver Protection,Control Cholesterol'
    )
    Product.objects.create(
        category=tea_cat,
        name='Fat Burner - Fat Cutter Tea',
        description='Weight control - Fat Loss, Cure constipation, Burn calorie, Improve digestion, Detoxification, Boost immune.',
        price=499, offer_price=430, weight='100GM',
        benefits='Weight control,Cure constipation,Burn calorie,Improve digestion,Detoxification,Boost immune'
    )
    Product.objects.create(
        category=tea_cat,
        name='Tummy Fat - Detox Tea',
        description='Weight control - Fat Loss, Fight inflammation, Burn calorie, Improve digestion, Boost energy, Water retention.',
        price=499, offer_price=399, weight='30 Tea Bags',
        benefits='Weight control,Fight inflammation,Burn calorie,Improve digestion,Boost energy,Water retention'
    )
    Product.objects.create(
        category=tea_cat,
        name='Skin & Hair Care - Ever Youthful Tea',
        description='Skin Detox, Collagen Boost, Natural Skin Glow, Dark Spots Remove, Suntan removes, Healthy Hair.',
        price=499, offer_price=430, weight='100GM',
        benefits='Skin Detox,Collagen Boost,Natural Skin Glow,Dark Spots Remove,Suntan removes,Healthy Hair'
    )
    Product.objects.create(
        category=tea_cat,
        name='Women Care Tea - PCOD / PCOS',
        description='100% Natural ingredients, Zero side effects.',
        price=400, offer_price=400, weight='100GM',
        benefits='PCOD care,PCOS care'
    )
    Product.objects.create(
        category=tea_cat,
        name='Good Night Tea',
        description='Reduces Stress, Reduces Anxiety, Promotes Sleep, Improve digestion, Reduces Dark Circles under eye, Control Blood Sugar Level.',
        price=250, offer_price=250, weight='50GM',
        benefits='Reduces Stress,Reduces Anxiety,Promotes Sleep,Improve digestion,Reduces Dark Circles,Control Blood Sugar Level'
    )
    Product.objects.create(
        category=tea_cat,
        name='Kashmiri Kahwa - Immunity Boost',
        description='Immunity Boost. 100% Natural ingredients.',
        price=399, offer_price=299, weight='20 Tea Bags',
        benefits='Immunity Boost'
    )
    
    # Drinks
    Product.objects.create(
        category=drink_cat,
        name='Gut Health Drink - Morning Detox',
        description='Weight management, Cure constipation, Improve digestion, Detoxification, Reduces Inflammation.',
        price=349, offer_price=250, weight='130GM',
        benefits='Weight management,Cure constipation,Improve digestion,Detoxification,Reduces Inflammation'
    )
    
    # Protein
    Product.objects.create(
        category=protein_cat,
        name='Sattu Pre-Mix',
        description='100% Natural, Zero Preservatives & Chemical, Gluten Free. Ingredients: Roasted Gram flour, Mint leaves, Cumin seeds, Coriander seeds, black pepper, Saunf, Dried mango, Chilli, Pink salt, Black salt.',
        price=220, offer_price=180, weight='250GM',
        benefits='Plant based Protein,Gluten Free'
    )

    print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
