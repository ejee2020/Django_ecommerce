from .models import Product

def subject_renderer(request):
    products = Product.objects.all()
    return {'all_subjects'}