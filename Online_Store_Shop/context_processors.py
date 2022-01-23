from Product.models import Category


def show_category(request):
    return {"p_category": list(Category.objects.filter(cat__isnull=True))}
