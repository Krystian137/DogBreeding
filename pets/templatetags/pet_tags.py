# pets/templatetags/pets_tags.py

from django import template
from pets.models import Dog, Litter

register = template.Library()


@register.simple_tag
def get_dogs_for_menu():
    """
    Get dogs for dropdown menu.
    Returns max 10 dogs from kennel (show_in_list=True, with slug).
    Returns empty queryset if none exist.
    """
    return Dog.objects.filter(
        show_in_list=True,
        slug__isnull=False
    ).exclude(
        slug=''
    ).order_by('name')[:10]


@register.simple_tag
def get_litters_for_menu():
    """
    Get litters for dropdown menu.
    Returns max 10 most recent litters.
    Returns empty queryset if none exist.
    """
    return Litter.objects.all().order_by('-birth_date')[:10]


@register.simple_tag
def has_dogs_in_menu():
    """
    Check if there are any dogs to show in menu.
    Returns True if at least one dog exists, False otherwise.
    """
    return Dog.objects.filter(
        show_in_list=True,
        slug__isnull=False
    ).exclude(slug='').exists()


@register.simple_tag
def has_litters_in_menu():
    """
    Check if there are any litters to show in menu.
    Returns True if at least one litter exists, False otherwise.
    """
    return Litter.objects.exists()