from Product.models import Category


def show_category():
    return Category.objects.filter(cat__isnull=True)