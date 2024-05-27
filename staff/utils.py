import random
import string
from django.core.cache import cache
from django.contrib.auth.models import Permission

from .variables import PermissionsByGroupName

def generate_password(length=12):
    """Generate a random password with the specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def get_permissions_by_group_name(group_name):
    permissions = cache.get(f'permissions_{group_name}')
    if not permissions:
        perms = PermissionsByGroupName[group_name]
        permissions = Permission.objects.filter(codename__in=perms)
        cache.set(f'permissions_{group_name}', permissions, timeout=60*60)  # Cache for 1 hour
    return permissions
