from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product, Testimonial, SiteSetting
from .resources import CategoryResource, ProductResource, TestimonialResource, SiteSettingResource

# Admin Branding Titles
admin.site.site_header = "Fit & Fine Forever Admin"
admin.site.site_title = "Fit & Fine Forever Admin Portal"
admin.site.index_title = "Manage Products, Client Transformations & Site Settings"

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('image_preview', 'name', 'category', 'subtitle_tag', 'price', 'offer_price', 'is_popular', 'order')
    list_editable = ('price', 'offer_price', 'is_popular', 'order')
    list_filter = ('category', 'is_popular')
    search_fields = ('name', 'description', 'benefits')
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'subtitle_tag', 'description', 'order', 'is_popular')
        }),
        ('Pricing & Package Options', {
            'fields': ('price', 'offer_price', 'weight', 'weight_options')
        }),
        ('Key Benefits & Media', {
            'fields': ('benefits', 'image', 'image_url')
        }),
    )

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 8px; border: 1px solid #ccc;" />', url)
        return "No Image"
    image_preview.short_description = "Preview"

@admin.register(Testimonial)
class TestimonialAdmin(ImportExportModelAdmin):
    resource_class = TestimonialResource
    list_display = ('image_preview', 'client_name', 'subtitle', 'rating', 'is_active', 'order')
    list_editable = ('rating', 'is_active', 'order')
    list_filter = ('is_active', 'rating')
    search_fields = ('client_name', 'subtitle', 'review_text')

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html('<img src="{}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 8px; border: 1px solid #ccc;" />', url)
        return "No Image"
    image_preview.short_description = "Preview"

@admin.register(SiteSetting)
class SiteSettingAdmin(ImportExportModelAdmin):
    resource_class = SiteSettingResource
    list_display = ('founder_name', 'about_title', 'whatsapp_number', 'founder_preview', 'hero_preview')
    
    fieldsets = (
        ('Founder Profile Settings', {
            'fields': ('founder_name', 'founder_image', 'about_title', 'about_text')
        }),
        ('Hero Banner Settings', {
            'fields': ('hero_image',)
        }),
        ('Contact & WhatsApp Settings', {
            'fields': ('whatsapp_number',),
            'description': 'This number is used for every WhatsApp button on the website (wa.me links).'
        }),
    )

    def founder_preview(self, obj):
        url = obj.get_founder_image()
        if url:
            return format_html('<img src="{}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 50%; border: 2px solid #C69C6D;" />', url)
        return "No Image"
    founder_preview.short_description = "Founder Photo"

    def hero_preview(self, obj):
        url = obj.get_hero_image()
        if url:
            return format_html('<img src="{}" style="width: 90px; height: 55px; object-fit: cover; border-radius: 8px; border: 1px solid #ccc;" />', url)
        return "No Image"
    hero_preview.short_description = "Hero Banner Photo"


