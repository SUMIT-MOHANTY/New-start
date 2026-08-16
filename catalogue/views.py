from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Testimonial, SiteSetting

def index(request):
    categories = Category.objects.prefetch_related('products').all()
    testimonials = Testimonial.objects.filter(is_active=True).all()
    site_setting = SiteSetting.objects.first()
    # Consultation pricing is managed via the 'Diet Consultation' product in admin.
    # Fallbacks only apply if that product is missing/deleted.
    consultation_product = Product.objects.filter(category__slug='diet-consultation').first()
    consultation_price = consultation_product.offer_price if consultation_product and consultation_product.offer_price else 799
    consultation_mrp = consultation_product.price if consultation_product and consultation_product.price else 999
    return render(request, 'catalogue/index.html', {
        'categories': categories,
        'testimonials': testimonials,
        'site_setting': site_setting,
        'consultation_price': consultation_price,
        'consultation_mrp': consultation_mrp,
        'whatsapp_number': site_setting.get_whatsapp_number() if site_setting else '919007104448',
        'whatsapp_display': site_setting.get_whatsapp_display() if site_setting else '+91 9007104448',
    })

def demo(request):
    return render(request, 'catalogue/demo.html')

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or non-staff user.')
            
    return render(request, 'catalogue/dashboard_login.html')

@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    site_setting, _ = SiteSetting.objects.get_or_create(id=1)

    if request.method == 'POST':
        action = request.POST.get('action')

        # Action 1: Update Site Settings
        if action == 'update_settings':
            site_setting.founder_name = request.POST.get('founder_name', site_setting.founder_name)
            site_setting.about_title = request.POST.get('about_title', site_setting.about_title)
            site_setting.about_text = request.POST.get('about_text', site_setting.about_text)
            if request.POST.get('whatsapp_number'):
                site_setting.whatsapp_number = request.POST.get('whatsapp_number')

            if 'hero_image' in request.FILES:
                site_setting.hero_image = request.FILES['hero_image']
            if 'founder_image' in request.FILES:
                site_setting.founder_image = request.FILES['founder_image']

            site_setting.save()
            messages.success(request, 'Site settings updated successfully!')

        # Action 2: Add Product
        elif action == 'add_product':
            cat_id = request.POST.get('category')
            category = Category.objects.get(id=cat_id)
            p = Product.objects.create(
                name=request.POST.get('name'),
                category=category,
                price=request.POST.get('price') or 0,
                offer_price=request.POST.get('offer_price') or None,
                subtitle_tag=request.POST.get('subtitle_tag', ''),
                description=request.POST.get('description', ''),
                benefits=request.POST.get('benefits', ''),
            )
            if 'image' in request.FILES:
                p.image = request.FILES['image']
                p.save()
            messages.success(request, f'Product "{p.name}" added successfully!')

        # Action 3: Edit Product
        elif action == 'edit_product':
            p = get_object_or_404(Product, id=request.POST.get('product_id'))
            p.name = request.POST.get('name', p.name)
            p.price = request.POST.get('price', p.price)
            if request.POST.get('offer_price'):
                p.offer_price = request.POST.get('offer_price')
            else:
                p.offer_price = None
            p.subtitle_tag = request.POST.get('subtitle_tag', p.subtitle_tag)
            p.description = request.POST.get('description', p.description)
            if 'image' in request.FILES:
                p.image = request.FILES['image']
            p.save()
            messages.success(request, f'Product "{p.name}" updated successfully!')

        # Action 4: Delete Product
        elif action == 'delete_product':
            p = get_object_or_404(Product, id=request.POST.get('product_id'))
            p_name = p.name
            p.delete()
            messages.success(request, f'Product "{p_name}" deleted successfully!')

        # Action 5: Add Transformation Testimonial
        elif action == 'add_testimonial':
            t = Testimonial.objects.create(
                client_name=request.POST.get('client_name'),
                subtitle=request.POST.get('subtitle', ''),
                rating=request.POST.get('rating', 5),
                is_active=True
            )
            if 'image' in request.FILES:
                t.image = request.FILES['image']
                t.save()
            messages.success(request, f'Client result for "{t.client_name}" added successfully!')

        return redirect('admin_dashboard')

    categories = Category.objects.all()
    products = Product.objects.select_related('category').all().order_by('-id')
    testimonials = Testimonial.objects.all().order_by('-id')

    return render(request, 'catalogue/dashboard.html', {
        'site_setting': site_setting,
        'categories': categories,
        'products': products,
        'testimonials': testimonials,
    })
