from django.shortcuts import render
from .models import Category, Product

def index(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'catalogue/index.html', {'categories': categories})
