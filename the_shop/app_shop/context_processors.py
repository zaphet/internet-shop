from django.db.models import Count

from .models import ProductCategory, SiteSettings


def categories(request):
    category_set = ProductCategory.objects.annotate(Count('products')).filter(is_active=True, products__gt=0).order_by('sorting_index')
    return {
        'categories': category_set
    }


def load_settings(request):
    return {'site_settings': SiteSettings.load()}
