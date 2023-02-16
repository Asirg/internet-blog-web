from blog.models import Category

def category_by_kwargs(kwargs: dict) -> Category:
    return Category.objects.get(url=kwargs.get('url'))