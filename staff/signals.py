from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group, Permission

from .utils import get_permissions_by_group_name
from .models import Staff

@receiver(post_save, sender=Staff)
def apply_group_to_user(sender, instance, created, **kwargs):
    groups_by_role = {
        1: "Mudir",
        2: "Katta hamshira", 
        8: "Resurs nazoratchisi"
    }
    if created:
        if instance.role in groups_by_role.keys():
            group_name = groups_by_role[instance.role]
            assign_group(instance, group_name)
            instance.save()

@receiver(pre_save, sender=Staff)
def apply_group_to_user_presave(sender, instance, **kwargs):
    groups_by_role = {
        1: "Mudir",
        2: "Katta hamshira", 
        8: "Resurs nazoratchisi"
    }
    if instance.pk:
        previous_staff = Staff.objects.get(pk=instance.pk)
        if previous_staff.groups.exists():
            instance.groups.clear()
            if instance.role not in groups_by_role.keys() and instance.is_staff:
                instance.is_staff=False
        if instance.role in groups_by_role.keys():
            group_name = groups_by_role[instance.role]
            assign_group(instance, group_name)

def assign_group(instance, group_name):
    instance.is_staff = True
    group, group_created = Group.objects.get_or_create(name=group_name)
    if group_created:
        permissions = get_permissions_by_group_name(group_name)
        group.permissions.add(*permissions)
    instance.groups.add(group)
