from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    subtitle_tag = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Immunity Boost, PCOD Care")
    description = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True, help_text="Comma separated list of benefits")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight_options = models.CharField(max_length=200, blank=True, null=True, help_text="e.g. 70g (₹349), 100g (₹499), 150g (₹799)")
    weight = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name}"

    def get_benefits_list(self):
        if self.benefits:
            return [b.strip() for b in self.benefits.split(',') if b.strip()]
        return []

    def get_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return '/static/img/placeholder.png'


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100, default="Happy Client")
    subtitle = models.CharField(max_length=150, blank=True, null=True, help_text="e.g. Weight Loss Transformation")
    review_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    rating = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"Testimonial - {self.client_name}"

    def get_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return ''

class SiteSetting(models.Model):
    about_title = models.CharField(max_length=200, default="About Fit & Fine Forever")
    about_text = models.TextField(blank=True, null=True)
    founder_name = models.CharField(max_length=100, default="Nutritionist Debasmita")
    founder_image = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    whatsapp_number = models.CharField(
        max_length=20,
        default="919007104448",
        help_text="WhatsApp number in international format without + or spaces, e.g. 919007104448",
    )

    def __str__(self):
        return "Site Settings"

    def get_founder_image(self):
        if self.founder_image:
            return self.founder_image.url
        return '/static/img/placeholder.png'

    def get_hero_image(self):
        if self.hero_image:
            return self.hero_image.url
        return '/static/img/doc_images/image2.png'

    def get_whatsapp_number(self):
        """Return the digits-only WhatsApp number for use in wa.me links."""
        digits = ''.join(c for c in (self.whatsapp_number or '') if c.isdigit())
        return digits or '919007104448'

    def get_whatsapp_display(self):
        """Pretty display format, e.g. +91 9007104448."""
        num = self.get_whatsapp_number()
        if num.startswith('91') and len(num) == 12:
            return f"+91 {num[2:]}"
        return f"+{num}"
