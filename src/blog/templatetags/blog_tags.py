from django import template

from blog.models import Category, Post


register = template.Library()

@register.simple_tag()
def link_page_with_args(page, args):
    link = f"?page={page}&"
    if args:
        for key, value in args.items():
            if value != [] and value != '':
                if type(value) == list:
                    link += '&'.join([
                        f'{key}={val}' for val in value
                    ])
                else:
                    link += f"{key}={value}"
                link += "&"
    return link

@register.simple_tag()
def get_main_categories():
    return Category.objects.filter(parent__isnull=True)