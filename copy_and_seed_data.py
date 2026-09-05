import os
import shutil
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fit_and_fine.settings')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from catalogue.models import Category, Product, Testimonial, SiteSetting

BASE_DIR = Path(__file__).resolve().parent

def run():
    print("--- Starting PDF Catalogue Sync and DB Seeding ---")
    
    # 1. Target Directories
    media_prod_dir = Path(settings.MEDIA_ROOT) / 'products'
    media_test_dir = Path(settings.MEDIA_ROOT) / 'testimonials'
    static_img_dir = BASE_DIR / 'static' / 'img' / 'doc_images'
    
    os.makedirs(media_prod_dir, exist_ok=True)
    os.makedirs(media_test_dir, exist_ok=True)
    os.makedirs(static_img_dir, exist_ok=True)

    # 2. Copy static images to media/products so Railway always has images on redeploy
    if static_img_dir.exists():
        for item in static_img_dir.glob('*'):
            dest_prod = media_prod_dir / item.name
            shutil.copy(item, dest_prod)
        print(f"Synced {len(list(static_img_dir.glob('*')))} product images to media/products.")

    # 3. Copy Testimonial Images
    orig_test_dir = media_prod_dir / 'Testimonials'
    testimonial_files = []
    if orig_test_dir.exists():
        for item in orig_test_dir.glob('*.jpeg'):
            dest = media_test_dir / item.name
            shutil.copy(item, dest)
            testimonial_files.append(f"/media/testimonials/{item.name}")

    # 4. Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    # 5. Clear Old Products & Categories
    Product.objects.all().delete()
    Category.objects.all().delete()

    # 6. Create Categories according to PDF
    wellness_tea = Category.objects.create(
        name='Wellness Teas',
        slug='wellness-teas',
        description='100% Natural, targeted herbal teas with zero side effects. Available in loose leaf & plastic-free tea bags.',
        order=1
    )
    flavour_tea = Category.objects.create(
        name='Flavour & Immunity Teas',
        slug='flavour-teas',
        description='Aromatic teas, saffron kahwa & spiced blends for immunity and refreshing daily health.',
        order=2
    )
    protein_cat = Category.objects.create(
        name='Plant Based Protein',
        slug='plant-protein',
        description='100% Natural, chemical-free, gluten-free traditional protein superfood mix.',
        order=3
    )
    health_drinks = Category.objects.create(
        name='Health Drinks & Detox',
        slug='health-drinks',
        description='Morning detox powders and cellular gut restoration drinks.',
        order=4
    )
    body_care = Category.objects.create(
        name='Body Care & Oils',
        slug='body-care',
        description='100% Herbal body firming and localized fat reduction oils.',
        order=5
    )
    combo_offers = Category.objects.create(
        name='Combo Offers',
        slug='combo-offers',
        description='Special discounted value packages & transformation kits.',
        order=6
    )
    consultation_cat = Category.objects.create(
        name='Diet Consultation',
        slug='diet-consultation',
        description='Personalized 45-day diet plans tailored by Nutritionist Debasmita Chandra.',
        order=7
    )

    tea_standard_weights = "70g (₹349) | 100g (₹499) | 150g (₹749) | 30 Tea Bags (₹499) | 60 Tea Bags (₹980)"

    # 7. Products Seed Data according to Fit & Fine Forever PDF
    products_data = [
        # --- Wellness Teas ---
        {
            'category': wellness_tea,
            'name': 'Slimming Tea - Fat To Fab',
            'subtitle_tag': 'Slimming & Metabolism',
            'description': 'Targeted slimming herbal tea that boosts metabolism, reduces sugar cravings, improves digestion, manages weight, protects liver function, and controls cholesterol.',
            'benefits': 'Boosts Metabolism, Reduces Sugar Cravings, Improves Digestion, Weight Management, Liver Protection, Controls Cholesterol',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/static/img/doc_images/image3.jpeg', 'is_popular': True, 'order': 1
        },
        {
            'category': wellness_tea,
            'name': 'Fat Burner - Fat Cutter Tea',
            'subtitle_tag': 'Fat Loss & Detox',
            'description': 'Potent fat burning herbal tea that helps burn stubborn calories, cures constipation, improves digestion, aids fat loss, and boosts immune defense.',
            'benefits': 'Weight Control & Fat Loss, Cure Constipation, Burn Calorie, Improve Digestion, Detoxification, Boost Immunity',
            'price': 499, 'offer_price': 349, 'weight_options': '100g (₹499) | 200g (₹999) | 30 Tea Bags (₹499) | 60 Tea Bags (₹980)', 'weight': '100g / 200g / 30-60 Tea Bags',
            'image_url': '/static/img/doc_images/image4.jpeg', 'is_popular': True, 'order': 2
        },
        {
            'category': wellness_tea,
            'name': 'Tummy Fat - Detox Tea',
            'subtitle_tag': 'Abdominal Fat & Bloating',
            'description': 'Specially formulated detox tea to target abdominal fat, fight inflammation, burn extra calories, boost daily energy, and reduce water retention.',
            'benefits': 'Weight Control & Fat Loss, Fight Inflammation, Burn Calorie, Improve Digestion, Boost Energy, Reduce Water Retention',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/static/img/doc_images/image5.jpeg', 'is_popular': True, 'order': 3
        },
        {
            'category': wellness_tea,
            'name': 'Skin & Hair Care - Ever Youthful Tea',
            'subtitle_tag': 'Skin Glow & Anti-Aging',
            'description': 'Antioxidant-rich herbal blend designed for skin detox, collagen boosting, natural skin glow, dark spots removal, suntan repair, and healthy hair nourishment.',
            'benefits': 'Skin Detox, Collagen Boost, Natural Skin Glow, Dark Spots Removal, Suntan Removal, Healthy Hair',
            'price': 499, 'offer_price': 349, 'weight_options': '100g (₹499) | 30 Tea Bags (₹499) | 60 Tea Bags (₹980)', 'weight': '100g / 30-60 Tea Bags',
            'image_url': '/static/img/doc_images/image6.jpeg', 'is_popular': True, 'order': 4
        },
        {
            'category': wellness_tea,
            'name': 'Women Care Tea - PCOD / PCOS',
            'subtitle_tag': 'Hormone & Cycle Balance',
            'description': 'Hormone balancing natural herbal tea specially formulated for women to assist in managing PCOD/PCOS symptoms, regulating cycles, and reducing bloating.',
            'benefits': 'PCOD & PCOS Support, Hormone Regulation, Cycle Harmony, Reduces Bloating, Zero Side Effects',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/static/img/doc_images/image8.jpeg', 'is_popular': True, 'order': 5
        },
        {
            'category': wellness_tea,
            'name': 'Good Night Tea',
            'subtitle_tag': 'Sleep & Stress Relief',
            'description': 'Relaxing evening botanical infusion that reduces stress and anxiety, promotes deep peaceful sleep, improves digestion, controls blood sugar, and fades dark circles under eyes.',
            'benefits': 'Reduces Stress & Anxiety, Promotes Sleep, Improves Digestion, Fades Under-Eye Dark Circles, Controls Blood Sugar Level',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/static/img/doc_images/image9.jpeg', 'is_popular': False, 'order': 6
        },
        {
            'category': wellness_tea,
            'name': 'Diabetic Care Tea',
            'subtitle_tag': 'Blood Sugar Management',
            'description': 'Herbal tea blend crafted with natural glycemic regulators to assist in blood sugar balance, insulin sensitivity, and sugar craving control.',
            'benefits': 'Blood Sugar Control, Insulin Support, Glycemic Balance, Metabolism Aid',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/static/img/doc_images/image10.jpeg', 'is_popular': False, 'order': 7
        },
        {
            'category': wellness_tea,
            'name': 'Heart Care Tea',
            'subtitle_tag': 'Cardio & Cholesterol Care',
            'description': 'Cardiovascular support herbal tea loaded with natural flavonoids to promote healthy blood pressure, arterial health, and cholesterol regulation.',
            'benefits': 'Heart Support, Cholesterol Balance, Arterial Vitality, Antioxidant Protection',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/static/img/doc_images/image11.jpeg', 'is_popular': False, 'order': 8
        },
        {
            'category': wellness_tea,
            'name': 'Thyrocare Tea',
            'subtitle_tag': 'Thyroid Health',
            'description': 'Nourishing herbal tea created to support optimal thyroid function, boost sluggish metabolism, balance energy levels, and reduce tiredness.',
            'benefits': 'Thyroid Support, Metabolism Boost, Energy Restoration, Hormonal Support',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/static/img/doc_images/image12.jpeg', 'is_popular': False, 'order': 9
        },
        {
            'category': wellness_tea,
            'name': 'Moms Care Tea',
            'subtitle_tag': 'Postpartum & Nursing Support',
            'description': 'Gentle and soothing herbal tea blend for new mothers to promote postpartum recovery, natural lactation support, and gentle daily nourishment.',
            'benefits': 'Postpartum Recovery, Lactation Support, Gentle Vitality, Restorative Care',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/static/img/doc_images/image14.png', 'is_popular': False, 'order': 10
        },
        {
            'category': wellness_tea,
            'name': '2-In-1 Skin Glow Tea',
            'subtitle_tag': 'Radiance & Hydration',
            'description': 'Dual action skin formulation designed to brighten complexion, nourish skin layers, and combat oxidative stress.',
            'benefits': 'Skin Brightening, Deep Hydration, Anti-Aging, Radiance',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/static/img/doc_images/image7.jpeg', 'is_popular': False, 'order': 11
        },

        # --- Flavour & Immunity Teas ---
        {
            'category': flavour_tea,
            'name': 'Kashmiri Kahwa - Immunity Boost',
            'subtitle_tag': 'Saffron & Spices',
            'description': 'Authentic Kashmiri green tea infused with saffron strands, green cardamom, cinnamon, and spices for immune strength, warmth, and skin glow.',
            'benefits': 'Immunity Boost, Saffron Infused, Natural Antioxidants, Warmth & Vitality, Skin Glow',
            'price': 399, 'offer_price': 299, 'weight_options': '20 Tea Bags (₹299 - MRP ₹399) | 100g Loose (₹399)', 'weight': '20 Tea Bags / 100g',
            'image_url': '/static/img/doc_images/image16.png', 'is_popular': True, 'order': 12
        },
        {
            'category': flavour_tea,
            'name': 'Masala Milk Tea',
            'subtitle_tag': 'Aromatic Indian Spices',
            'description': 'Traditional black tea blend infused with aromatic hand-ground spices for an invigorating, comforting cup of authentic chai.',
            'benefits': 'Immunity Support, Digestive Aid, Rich Spice Flavor, Warm Comfort',
            'price': 199, 'offer_price': 199, 'weight_options': '100g (₹199)', 'weight': '100g',
            'image_url': '/static/img/doc_images/image15.png', 'is_popular': False, 'order': 13
        },
        {
            'category': flavour_tea,
            'name': 'Green Tea',
            'subtitle_tag': 'Pure Antioxidants',
            'description': 'Unprocessed green tea leaves packed with natural EGCG antioxidants for daily body detox, clean energy, and metabolic support.',
            'benefits': 'Antioxidant Rich, Metabolism Boost, Calorie Burn, Daily Detox',
            'price': 349, 'offer_price': 249, 'weight_options': '100g (₹249 - MRP ₹349)', 'weight': '100g',
            'image_url': '/static/img/doc_images/image17.png', 'is_popular': False, 'order': 14
        },
        {
            'category': flavour_tea,
            'name': 'Golden Darjeeling Tea',
            'subtitle_tag': 'Single Estate Muscadel',
            'description': 'Exquisite single-estate Darjeeling tea known as the champagne of teas, delivering a floral aroma and refined muscatel flavor.',
            'benefits': 'Refined Taste, Heart Health, Gentle Energy, Focus',
            'price': 499, 'offer_price': 399, 'weight_options': '100g (₹399 - MRP ₹499)', 'weight': '100g',
            'image_url': '/static/img/doc_images/image18.png', 'is_popular': False, 'order': 15
        },

        # --- Plant Based Protein ---
        {
            'category': protein_cat,
            'name': 'Sattu Pre-Mix',
            'subtitle_tag': 'Best Plant-Based Protein',
            'description': '100% natural, chemical-free, gluten-free traditional plant protein superfood drink mix made with roasted gram flour, mint leaves, cumin, coriander, black pepper, saunf, dry mango, chilli, pink salt & black salt. FSSAI Licensed (22824131000442).',
            'benefits': 'Plant Based Protein, 100% Natural, Zero Preservatives & Chemical, Gluten Free, Sustained Energy, Cooling Gut Support',
            'price': 220, 'offer_price': 199, 'weight_options': '250g (₹199 - MRP ₹220) | Combo Offer (₹380)', 'weight': '250g',
            'image_url': '/static/img/doc_images/sattu_mix.png', 'is_popular': True, 'order': 16
        },

        # --- Health Drinks & Detox ---
        {
            'category': health_drinks,
            'name': 'Gut Health Drink - Morning Detox',
            'subtitle_tag': 'Gut Restoration & Constipation Relief',
            'description': 'Potent morning detox drink mix that heals gut lining, relieves chronic constipation, improves digestion, aids weight management, and reduces systemic inflammation.',
            'benefits': 'Weight Management, Cure Constipation, Improve Digestion, Detoxification, Reduces Inflammation',
            'price': 349, 'offer_price': 250, 'weight_options': '130g (₹250 - MRP ₹349) | 250g (₹480 - MRP ₹670)', 'weight': '130g / 250g',
            'image_url': '/static/img/doc_images/gut_drink.png', 'is_popular': True, 'order': 17
        },

        # --- Body Care & Oils ---
        {
            'category': body_care,
            'name': 'Slimming Oil',
            'subtitle_tag': 'Localized Fat Burn & Firming',
            'description': '100% natural herbal oil blend formulated to stimulate localized blood circulation, reduce cellulite appearance, and firm loose skin tissue.',
            'benefits': 'Localized Fat Burn, Skin Firming, Cellulite Reduction, 100% Natural, Zero Side Effects',
            'price': 350, 'offer_price': 350, 'weight_options': '100ml (₹350) | 300ml (₹999)', 'weight': '100ml / 300ml',
            'image_url': '/static/img/doc_images/slimming_tea.png', 'is_popular': False, 'order': 18
        },

        # --- Combo Offers ---
        {
            'category': combo_offers,
            'name': 'Weight Loss Mega Combo',
            'subtitle_tag': 'Fat Loss & Detox Kit',
            'description': 'Comprehensive fat burning and detox package combining Fat Cutter Tea, Gut Health Detox Drink, and Slimming Tea for accelerated weight loss results.',
            'benefits': 'Complete Fat Loss Kit, Accelerated Detox, Synergistic Herbal Benefits, Maximum Savings',
            'price': 1400, 'offer_price': 1075, 'weight_options': 'Complete Kit (₹1075 - Save ₹325)', 'weight': 'Combo Pack',
            'image_url': '/static/img/doc_images/image2.png', 'is_popular': True, 'order': 19
        },
        {
            'category': combo_offers,
            'name': 'Starter Detox Combo',
            'subtitle_tag': 'Gut & Skin Renewal Kit',
            'description': 'Perfect starter wellness kit combining Gut Health Detox Drink and Ever Youthful Skin Tea for gut reset and radiant skin glow.',
            'benefits': 'Gut Reset, Skin Glow, Cellular Detox, Starter Discount',
            'price': 1100, 'offer_price': 825, 'weight_options': 'Starter Pack (₹825 - Save ₹275)', 'weight': 'Combo Pack',
            'image_url': '/static/img/doc_images/image1.png', 'is_popular': False, 'order': 20
        },
        {
            'category': combo_offers,
            'name': 'Ultimate Wellness Combo',
            'subtitle_tag': 'Total Body Transformation Pack',
            'description': 'Ultimate all-in-one wellness bundle featuring Wellness Tea, Sattu Protein Pre-Mix, Gut Detox Drink, and Slimming Oil for holistic health transform.',
            'benefits': 'Full Body Transformation, Hormonal & Digestive Support, Best Value Package',
            'price': 1800, 'offer_price': 1425, 'weight_options': 'Ultimate Kit (₹1425 - Save ₹375)', 'weight': 'Combo Pack',
            'image_url': '/static/img/doc_images/image2.png', 'is_popular': True, 'order': 21
        },

        # --- Diet Consultation ---
        {
            'category': consultation_cat,
            'name': '45 Days Personalized Diet Plan',
            'subtitle_tag': 'By Nutritionist Debasmita (12+ Yrs Exp)',
            'description': 'Debasmita’s diet plan heals your gut, detoxifies your cells, and restores your body\'s natural balance. Her easy-to-follow diet plans revolve around easy eating habits through only home cooked foods. Personalized guidance for Obesity, Weight Gain, Diabetes, Pregnancy, Hypertension, Thyroid, PCOD/PCOS, Pre-wedding diet, Skin & Hair. Includes recipe guidance, daily follow-ups, and workout advice.',
            'benefits': '100% Home Cooked Food, Gut Healing & Cell Detox, Daily Follow-ups, Disease & Weight Specialist, Lifestyle Guidance',
            'price': 999, 'offer_price': 799, 'weight_options': '45 Days Plan (₹799 - MRP ₹999)', 'weight': '45 Days Plan',
            'image_url': '/static/img/doc_images/diet_plan.png', 'is_popular': True, 'order': 22
        }
    ]

    for pdata in products_data:
        Product.objects.create(**pdata)
    print(f"Seeded {len(products_data)} products successfully according to Fit & Fine Forever PDF!")

    # 8. Testimonials Seed Data
    testimonials_data = [
        {
            'client_name': 'Ananya Roy',
            'subtitle': 'PCOD & Weight Loss Success',
            'review_text': 'Debasmita ma\'am guided me with simple home cooked diet plans. My PCOD symptoms improved drastically and I lost 7 kg in 2 months!',
            'image_url': testimonial_files[0] if len(testimonial_files) > 0 else '',
            'rating': 5, 'order': 1
        },
        {
            'client_name': 'Rajesh Sharma',
            'subtitle': 'Diabetes & Gut Detox',
            'review_text': 'The Gut Health Detox Drink combined with the personalized meal plan stabilized my blood sugar level naturally without rigid starvation.',
            'image_url': testimonial_files[1] if len(testimonial_files) > 1 else '',
            'rating': 5, 'order': 2
        },
        {
            'client_name': 'Sneha Chatterjee',
            'subtitle': 'Postpartum Health Recovery',
            'review_text': 'I was struggling with low energy and weight gain post pregnancy. Debasmita\'s care and natural teas brought back my strength and skin glow.',
            'image_url': testimonial_files[2] if len(testimonial_files) > 2 else '',
            'rating': 5, 'order': 3
        },
        {
            'client_name': 'Pooja Verma',
            'subtitle': 'Skin Glow & Thyroid Management',
            'review_text': 'Ever Youthful Tea and Thyrocare Tea have done wonders for my skin pigmentation and thyroid sluggishness. Highly recommended!',
            'image_url': testimonial_files[3] if len(testimonial_files) > 3 else '',
            'rating': 5, 'order': 4
        },
        {
            'client_name': 'Vikramaditya S.',
            'subtitle': 'Fat Cutter & Active Fitness',
            'review_text': 'Fat Cutter Tea along with Sattu Pre-mix gives amazing clean energy. Reduced tummy bloat in less than 3 weeks!',
            'image_url': testimonial_files[4] if len(testimonial_files) > 4 else '',
            'rating': 5, 'order': 5
        },
        {
            'client_name': 'Meera Sen',
            'subtitle': 'Hypertension & Weight Balance',
            'review_text': '100% natural, zero side effects. The daily follow-up from Debasmita kept me accountable throughout my transformation.',
            'image_url': testimonial_files[5] if len(testimonial_files) > 5 else '',
            'rating': 5, 'order': 6
        },
        {
            'client_name': 'Ritu Mukherjee',
            'subtitle': 'Healthy Lifestyle Routine',
            'review_text': 'No artificial supplements, only home cooked food and effective tea blends. Truly a life-changing experience!',
            'image_url': testimonial_files[6] if len(testimonial_files) > 6 else '',
            'rating': 5, 'order': 7
        },
        {
            'client_name': 'Priyanka Das',
            'subtitle': 'Inflammation & Radiant Skin',
            'review_text': 'The 2-in-1 Skin Glow tea and personalized consultation transformed my hair texture and reduced facial inflammation.',
            'image_url': testimonial_files[7] if len(testimonial_files) > 7 else '',
            'rating': 5, 'order': 8
        }
    ]

    for tdata in testimonials_data:
        Testimonial.objects.create(**tdata)
    print(f"Seeded {len(testimonials_data)} testimonials successfully.")

    print("--- PDF Catalogue Sync Complete! ---")

if __name__ == '__main__':
    run()
