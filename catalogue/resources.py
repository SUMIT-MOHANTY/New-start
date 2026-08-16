from import_export import fields, resources
from import_export.widgets import CharWidget, ForeignKeyWidget
from .models import Category, Product, Testimonial, SiteSetting


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'order')
        import_id_fields = ('id',)


class ProductResource(resources.ModelResource):
    # Export/import the stored image filename (e.g. products/foo.jpg) as text.
    # The actual file lives on the persistent volume, so this restores the
    # reference without needing the binary in the CSV.
    image = fields.Field(attribute='image', column_name='image', widget=CharWidget())

    # Show/accept the category by NAME (readable in Excel), not numeric id.
    # Import categories first, then products, so the names resolve.
    category = fields.Field(
        attribute='category', column_name='category',
        widget=ForeignKeyWidget(Category, field='name'),
    )

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'subtitle_tag', 'description', 'benefits',
                  'price', 'offer_price', 'weight_options', 'weight',
                  'is_popular', 'order', 'image_url', 'image')
        import_id_fields = ('id',)


class TestimonialResource(resources.ModelResource):
    image = fields.Field(attribute='image', column_name='image', widget=CharWidget())

    class Meta:
        model = Testimonial
        fields = ('id', 'client_name', 'subtitle', 'review_text', 'rating',
                  'is_active', 'order', 'image_url', 'image')
        import_id_fields = ('id',)


class SiteSettingResource(resources.ModelResource):
    class Meta:
        model = SiteSetting
        fields = ('id', 'about_title', 'about_text', 'founder_name', 'whatsapp_number')
        import_id_fields = ('id',)
