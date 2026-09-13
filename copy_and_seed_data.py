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
    static_img_dir = BASE_DIR / 'static' / 'img' / 'doc_images'
    
    os.makedirs(media_prod_dir, exist_ok=True)
    os.makedirs(static_img_dir, exist_ok=True)

    # 2. Copy static images to media/products so Railway always has images on redeploy
    if static_img_dir.exists():
        for item in static_img_dir.glob('*'):
            dest_prod = media_prod_dir / item.name
            shutil.copy(item, dest_prod)
        print(f"Synced {len(list(static_img_dir.glob('*')))} product images to media/products.")

    # 4. Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@nutritionistdebasmita.com', 'AdminPass123!')

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
            'image_url': '/media/products/slimming_tea_fat_to_fab.jpeg', 'is_popular': True, 'order': 1
        },
        {
            'category': wellness_tea,
            'name': 'Fat Burner - Fat Cutter Tea',
            'subtitle_tag': 'Fat Loss & Detox',
            'description': 'Potent fat burning herbal tea that helps burn stubborn calories, cures constipation, improves digestion, aids fat loss, and boosts immune defense.',
            'benefits': 'Weight Control & Fat Loss, Cure Constipation, Burn Calorie, Improve Digestion, Detoxification, Boost Immunity',
            'price': 499, 'offer_price': 349, 'weight_options': '100g (₹499) | 200g (₹999) | 30 Tea Bags (₹499) | 60 Tea Bags (₹980)', 'weight': '100g / 200g / 30-60 Tea Bags',
            'image_url': '/media/products/fat_burner_fat_cutter_tea.jpeg', 'is_popular': True, 'order': 2
        },
        {
            'category': wellness_tea,
            'name': 'Tummy Fat - Detox Tea',
            'subtitle_tag': 'Abdominal Fat & Bloating',
            'description': 'Specially formulated detox tea to target abdominal fat, fight inflammation, burn extra calories, boost daily energy, and reduce water retention.',
            'benefits': 'Weight Control & Fat Loss, Fight Inflammation, Burn Calorie, Improve Digestion, Boost Energy, Reduce Water Retention',
            'price': 499, 'offer_price': 499, 'weight_options': '30 Tea Bags (₹499) | 60 Tea Bags (₹980)', 'weight': '30 Tea Bags / 60 Tea Bags',
            'image_url': '/media/products/tummy_fat_detox_tea.jpeg', 'is_popular': True, 'order': 3
        },
        {
            'category': wellness_tea,
            'name': 'Skin & Hair Care - Ever Youthful Tea',
            'subtitle_tag': 'Skin Glow & Anti-Aging',
            'description': 'Antioxidant-rich herbal blend designed for skin detox, collagen boosting, natural skin glow, dark spots removal, suntan repair, and healthy hair nourishment.',
            'benefits': 'Skin Detox, Collagen Boost, Natural Skin Glow, Dark Spots Removal, Suntan Removal, Healthy Hair',
            'price': 499, 'offer_price': 349, 'weight_options': '100g (₹499) | 30 Tea Bags (₹499) | 60 Tea Bags (₹980)', 'weight': '100g / 30-60 Tea Bags',
            'image_url': '/media/products/ever_youthful_tea.jpeg', 'is_popular': True, 'order': 4
        },
        {
            'category': wellness_tea,
            'name': 'Women Care Tea - PCOD / PCOS',
            'subtitle_tag': 'Hormone & Cycle Balance',
            'description': 'Hormone balancing natural herbal tea specially formulated for women to assist in managing PCOD/PCOS symptoms, regulating cycles, and reducing bloating.',
            'benefits': 'PCOD & PCOS Support, Hormone Regulation, Cycle Harmony, Reduces Bloating, Zero Side Effects',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/media/products/women_care_tea.jpeg', 'is_popular': True, 'order': 5
        },
        {
            'category': wellness_tea,
            'name': 'Good Night Tea',
            'subtitle_tag': 'Sleep & Stress Relief',
            'description': 'Relaxing evening botanical infusion that reduces stress and anxiety, promotes deep peaceful sleep, improves digestion, controls blood sugar, and fades dark circles under eyes.',
            'benefits': 'Reduces Stress & Anxiety, Promotes Sleep, Improves Digestion, Fades Under-Eye Dark Circles, Controls Blood Sugar Level',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/media/products/good_night_tea.jpeg', 'is_popular': False, 'order': 6
        },
        {
            'category': wellness_tea,
            'name': 'Diabetic Care Tea',
            'subtitle_tag': 'Blood Sugar Management',
            'description': 'Herbal tea blend crafted with natural glycemic regulators to assist in blood sugar balance, insulin sensitivity, and sugar craving control.',
            'benefits': 'Blood Sugar Control, Insulin Support, Glycemic Balance, Metabolism Aid',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/media/products/diabetic_care_tea.jpeg', 'is_popular': False, 'order': 7
        },
        {
            'category': wellness_tea,
            'name': 'Heart Care Tea',
            'subtitle_tag': 'Cardio & Cholesterol Care',
            'description': 'Cardiovascular support herbal tea loaded with natural flavonoids to promote healthy blood pressure, arterial health, and cholesterol regulation.',
            'benefits': 'Heart Support, Cholesterol Balance, Arterial Vitality, Antioxidant Protection',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/media/products/heart_care_tea.jpeg', 'is_popular': False, 'order': 8
        },
        {
            'category': wellness_tea,
            'name': 'Thyrocare Tea',
            'subtitle_tag': 'Thyroid Health',
            'description': 'Nourishing herbal tea created to support optimal thyroid function, boost sluggish metabolism, balance energy levels, and reduce tiredness.',
            'benefits': 'Thyroid Support, Metabolism Boost, Energy Restoration, Hormonal Support',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/media/products/thyrocare_tea.jpeg', 'is_popular': False, 'order': 9
        },
        {
            'category': wellness_tea,
            'name': 'Moms Care Tea',
            'subtitle_tag': 'Postpartum & Nursing Support',
            'description': 'Gentle and soothing herbal tea blend for new mothers to promote postpartum recovery, natural lactation support, and gentle daily nourishment.',
            'benefits': 'Postpartum Recovery, Lactation Support, Gentle Vitality, Restorative Care',
            'price': 499, 'offer_price': 349, 'weight_options': '70g (₹349) | 100g (₹499) | 150g (₹749)', 'weight': '70g / 100g / 150g',
            'image_url': '/media/products/moms_care_post_pregnancy_tea.jpeg', 'is_popular': False, 'order': 10
        },
        {
            'category': wellness_tea,
            'name': '2-In-1 Skin Glow Tea',
            'subtitle_tag': 'Radiance & Hydration',
            'description': 'Dual action skin formulation designed to brighten complexion, nourish skin layers, and combat oxidative stress.',
            'benefits': 'Skin Brightening, Deep Hydration, Anti-Aging, Radiance',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/media/products/2in1_skin_glow_tea.jpeg', 'is_popular': False, 'order': 11
        },
        {
            'category': wellness_tea,
            'name': 'Energy Boost Tea',
            'subtitle_tag': 'Focus & Daily Vitality',
            'description': 'Revitalizing botanical blend formulated to boost mental focus, sustain natural energy levels, relieve stress, and enhance daily stamina.',
            'benefits': 'Focus & Energy Boost, Stress Relief, Natural Vitality, Daily Stamina',
            'price': 499, 'offer_price': 349, 'weight_options': tea_standard_weights, 'weight': '70g / 100g / 150g / 30-60 Tea Bags',
            'image_url': '/media/products/energy_boost_tea.jpeg', 'is_popular': True, 'order': 12
        },

        # --- Flavour & Immunity Teas ---
        {
            'category': flavour_tea,
            'name': 'Kashmiri Kahwa - Immunity Boost',
            'subtitle_tag': 'Saffron & Spices',
            'description': 'Authentic Kashmiri green tea infused with saffron strands, green cardamom, cinnamon, and spices for immune strength, warmth, and skin glow.',
            'benefits': 'Immunity Boost, Saffron Infused, Natural Antioxidants, Warmth & Vitality, Skin Glow',
            'price': 399, 'offer_price': 299, 'weight_options': '20 Tea Bags (₹299 - MRP ₹399) | 100g Loose (₹399)', 'weight': '20 Tea Bags / 100g',
            'image_url': '/media/products/kashmiri_kahwa.jpeg', 'is_popular': True, 'order': 13
        },
        {
            'category': flavour_tea,
            'name': 'Darjeeling Kadak Tea',
            'subtitle_tag': 'Aromatic Indian Spices',
            'description': 'Traditional black tea blend infused with aromatic hand-ground spices for an invigorating, comforting cup of authentic chai.',
            'benefits': 'Immunity Support, Digestive Aid, Rich Spice Flavor, Warm Comfort',
            'price': 199, 'offer_price': 199, 'weight_options': '100g (₹199)', 'weight': '100g',
            'image_url': '/media/products/masala_darjeeling_tea.jpeg', 'is_popular': False, 'order': 14
        },
        {
            'category': flavour_tea,
            'name': 'Darjeeling Green Tea',
            'subtitle_tag': 'Pure Antioxidants',
            'description': 'Unprocessed green tea leaves packed with natural EGCG antioxidants for daily body detox, clean energy, and metabolic support.',
            'benefits': 'Antioxidant Rich, Metabolism Boost, Calorie Burn, Daily Detox',
            'price': 349, 'offer_price': 249, 'weight_options': '100g (₹249 - MRP ₹349)', 'weight': '100g',
            'image_url': '/media/products/darjeeling_green_tea.jpeg', 'is_popular': False, 'order': 15
        },
        {
            'category': flavour_tea,
            'name': 'Golden Darjeeling Tea',
            'subtitle_tag': 'Single Estate Muscadel',
            'description': 'Exquisite single-estate Darjeeling tea known as the champagne of teas, delivering a floral aroma and refined muscatel flavor.',
            'benefits': 'Refined Taste, Heart Health, Gentle Energy, Focus',
            'price': 499, 'offer_price': 399, 'weight_options': '100g (₹399 - MRP ₹499)', 'weight': '100g',
            'image_url': '/media/products/golden_darjeeling_tea.jpeg', 'is_popular': False, 'order': 16
        },

        # --- Plant Based Protein ---
        {
            'category': protein_cat,
            'name': 'Sattu Pre-Mix',
            'subtitle_tag': 'Best Plant-Based Protein',
            'description': '100% natural, chemical-free, gluten-free traditional plant protein superfood drink mix made with roasted gram flour, mint leaves, cumin, coriander, black pepper, saunf, dry mango, chilli, pink salt & black salt. FSSAI Licensed (22824131000442).',
            'benefits': 'Plant Based Protein, 100% Natural, Zero Preservatives & Chemical, Gluten Free, Sustained Energy, Cooling Gut Support',
            'price': 249, 'offer_price': 249, 'weight_options': '250g (₹249) | Combo Offer (₹449)', 'weight': '250g / Combo Offer',
            'image_url': '/media/products/sattu_pre_mix.jpeg', 'is_popular': True, 'order': 17
        },

        # --- Health Drinks & Detox ---
        {
            'category': health_drinks,
            'name': 'Gut Health Drink - Morning Detox',
            'subtitle_tag': 'Gut Restoration & Constipation Relief',
            'description': 'Potent morning detox drink mix that heals gut lining, relieves chronic constipation, improves digestion, aids weight management, and reduces systemic inflammation.',
            'benefits': 'Weight Management, Cure Constipation, Improve Digestion, Detoxification, Reduces Inflammation',
            'price': 299, 'offer_price': 299, 'weight_options': '130g (₹299) | 250g (₹549)', 'weight': '130g / 250g',
            'image_url': '/media/products/gut_health_detox_drink.jpeg', 'is_popular': True, 'order': 18
        },

        # --- Body Care & Oils ---
        {
            'category': body_care,
            'name': 'Slimming Oil',
            'subtitle_tag': 'Localized Fat Burn & Firming',
            'description': '100% natural herbal oil blend formulated to stimulate localized blood circulation, reduce cellulite appearance, and firm loose skin tissue.',
            'benefits': 'Localized Fat Burn, Skin Firming, Cellulite Reduction, 100% Natural, Zero Side Effects',
            'price': 399, 'offer_price': 399, 'weight_options': '100ml (₹399) | 300ml (₹1155)', 'weight': '100ml / 300ml',
            'image_url': '/media/products/slimming_oil.jpeg', 'is_popular': False, 'order': 19
        },

        # --- Combo Offers ---
        {
            'category': combo_offers,
            'name': 'Weight Loss Mega Combo',
            'subtitle_tag': 'Fat Loss & Detox Kit',
            'description': 'Comprehensive fat burning and detox package combining Fat Cutter Tea, Gut Health Detox Drink, and Slimming Tea for accelerated weight loss results.',
            'benefits': 'Complete Fat Loss Kit, Accelerated Detox, Synergistic Herbal Benefits, Maximum Savings',
            'price': 1400, 'offer_price': 1075, 'weight_options': 'Complete Kit (₹1075 - Save ₹325)', 'weight': 'Combo Pack',
            'image_url': '/static/img/doc_images/combo_mega.jpg', 'is_popular': True, 'order': 20
        },
        {
            'category': combo_offers,
            'name': 'Starter Detox Combo',
            'subtitle_tag': 'Gut & Skin Renewal Kit',
            'description': 'Perfect starter wellness kit combining Gut Health Detox Drink and Ever Youthful Skin Tea for gut reset and radiant skin glow.',
            'benefits': 'Gut Reset, Skin Glow, Cellular Detox, Starter Discount',
            'price': 1100, 'offer_price': 825, 'weight_options': 'Starter Pack (₹825 - Save ₹275)', 'weight': 'Combo Pack',
            'image_url': '/static/img/doc_images/combo_starter.jpg', 'is_popular': False, 'order': 21
        },
        {
            'category': combo_offers,
            'name': 'Ultimate Wellness Combo',
            'subtitle_tag': 'Total Body Transformation Pack',
            'description': 'Ultimate all-in-one wellness bundle featuring Wellness Tea, Sattu Protein Pre-Mix, Gut Detox Drink, and Slimming Oil for holistic health transform.',
            'benefits': 'Full Body Transformation, Hormonal & Digestive Support, Best Value Package',
            'price': 1800, 'offer_price': 1425, 'weight_options': 'Ultimate Kit (₹1425 - Save ₹375)', 'weight': 'Combo Pack',
            'image_url': '/static/img/doc_images/combo_ultimate.jpg', 'is_popular': True, 'order': 22
        },

        # --- Diet Consultation ---
        {
            'category': consultation_cat,
            'name': '45 Days Personalized Diet Plan',
            'subtitle_tag': 'By Nutritionist Debasmita (12+ Yrs Exp)',
            'description': 'Debasmita’s diet plan heals your gut, detoxifies your cells, and restores your body\'s natural balance. Her easy-to-follow diet plans revolve around easy eating habits through only home cooked foods. Personalized guidance for Obesity, Weight Gain, Diabetes, Pregnancy, Hypertension, Thyroid, PCOD/PCOS, Pre-wedding diet, Skin & Hair. Includes recipe guidance, daily follow-ups, and workout advice.',
            'benefits': '100% Home Cooked Food, Gut Healing & Cell Detox, Daily Follow-ups, Disease & Weight Specialist, Lifestyle Guidance',
            'price': 999, 'offer_price': 799, 'weight_options': '45 Days Plan (₹799 - MRP ₹999)', 'weight': '45 Days Plan',
            'image_url': '/static/img/doc_images/diet_plan.png', 'is_popular': True, 'order': 23
        }
    ]

    for pdata in products_data:
        Product.objects.create(**pdata)
    print(f"Seeded {len(products_data)} products successfully according to Fit & Fine Forever PDF!")

    # 8. Testimonials Seed Data
    # Client transformation photos ship with the code in static/ so they exist
    # on every deploy (media/ is gitignored and may not persist). Client names
    # are stored in the DB for admin reference but are NOT shown on the site.
    testimonials_data = [
        {
            'client_name': 'Ananya Roy',
            'subtitle': 'PCOD & Weight Loss Success',
            'review_text': 'Debasmita ma\'am guided me with simple home cooked diet plans. My PCOD symptoms improved drastically and I lost 7 kg in 2 months!',
            'image_url': '/static/img/testimonials/testimonial_1.jpeg',
            'rating': 5, 'order': 1
        },
        {
            'client_name': 'Rajesh Sharma',
            'subtitle': 'Diabetes & Gut Detox',
            'review_text': 'The Gut Health Detox Drink combined with the personalized meal plan stabilized my blood sugar level naturally without rigid starvation.',
            'image_url': '/static/img/testimonials/testimonial_2.jpeg',
            'rating': 5, 'order': 2
        },
        {
            'client_name': 'Sneha Chatterjee',
            'subtitle': 'Postpartum Health Recovery',
            'review_text': 'I was struggling with low energy and weight gain post pregnancy. Debasmita\'s care and natural teas brought back my strength and skin glow.',
            'image_url': '/static/img/testimonials/testimonial_3.jpeg',
            'rating': 5, 'order': 3
        },
        {
            'client_name': 'Pooja Verma',
            'subtitle': 'Skin Glow & Thyroid Management',
            'review_text': 'Ever Youthful Tea and Thyrocare Tea have done wonders for my skin pigmentation and thyroid sluggishness. Highly recommended!',
            'image_url': '/static/img/testimonials/testimonial_4.jpeg',
            'rating': 5, 'order': 4
        },
        {
            'client_name': 'Vikramaditya S.',
            'subtitle': 'Fat Cutter & Active Fitness',
            'review_text': 'Fat Cutter Tea along with Sattu Pre-mix gives amazing clean energy. Reduced tummy bloat in less than 3 weeks!',
            'image_url': '/static/img/testimonials/testimonial_5.jpeg',
            'rating': 5, 'order': 5
        },
        {
            'client_name': 'Meera Sen',
            'subtitle': 'Hypertension & Weight Balance',
            'review_text': '100% natural, zero side effects. The daily follow-up from Debasmita kept me accountable throughout my transformation.',
            'image_url': '/static/img/testimonials/testimonial_6.jpeg',
            'rating': 5, 'order': 6
        },
        {
            'client_name': 'Ritu Mukherjee',
            'subtitle': 'Healthy Lifestyle Routine',
            'review_text': 'No artificial supplements, only home cooked food and effective tea blends. Truly a life-changing experience!',
            'image_url': '/static/img/testimonials/testimonial_7.jpeg',
            'rating': 5, 'order': 7
        },
        {
            'client_name': 'Priyanka Das',
            'subtitle': 'Inflammation & Radiant Skin',
            'review_text': 'The 2-in-1 Skin Glow tea and personalized consultation transformed my hair texture and reduced facial inflammation.',
            'image_url': '/static/img/testimonials/testimonial_8.jpeg',
            'rating': 5, 'order': 8
        }
    ]

    # Idempotent: exactly one row per client, no matter how many times this
    # script runs (the old version created a fresh duplicate set on every
    # deploy). Rows added from the dashboard with new client names are kept.
    removed_dups = 0
    for tdata in testimonials_data:
        existing = Testimonial.objects.filter(client_name=tdata['client_name']).order_by('id')
        first = existing.first()
        if first:
            for dup in existing[1:]:
                dup.delete()
                removed_dups += 1
            for k, v in tdata.items():
                setattr(first, k, v)
            first.save()
        else:
            Testimonial.objects.create(**tdata)
    print(f"Seeded {len(testimonials_data)} testimonials successfully (idempotent, removed {removed_dups} duplicates).")

    # 9. Site Settings Seed Data
    setting, _ = SiteSetting.objects.get_or_create(id=1)
    setting.about_title = "About Fit & Fine Forever"
    setting.about_text = "<p>At Fit & Fine Forever, we believe that healthy eating should be simple, enjoyable, and accessible to everyone. Our mission is to help you nourish your body and mind by providing personalized meal plans, delicious recipes, and practical tools that fit your lifestyle.</p><p>Debasmita brings over 12 years of experience as a nutrition consultant and lifestyle coach. Whether you're a busy professional, a health enthusiast, or just starting your wellness journey — Fit & Fine Forever makes it easy to plan, prepare, and enjoy nutritious meals that fuel your day.</p>"
    setting.founder_name = "Nutritionist Debasmita"
    setting.hero_image = None
    setting.founder_image = None
    setting.save()
    print("Seeded SiteSetting successfully.")

    print("--- PDF Catalogue Sync Complete! ---")

if __name__ == '__main__':
    run()
