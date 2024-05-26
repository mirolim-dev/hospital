from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group, Permission

from .variables import PermissionsByGroupName
from .models import Staff

@receiver(post_save, sender=Staff)
def apply_group_to_user(sender, instance, **kwargs):
    """
        role choices: 
            (1, _("Mudir")),
            (2, _("Katta hamshira")),
            (3, _("Doctor")),
            (4, _("Hamshira")),
            (5, _("Farrosh")),
            (6, _("Qorovul")),
            (7, _("Haydovchi")),
            (8, _("Resurs nazoratchisi")),
    """
    if created:
        groups_by_role = {
            1: "Mudir",
            2: "Katta hamshira", 
            8: "Resurs nazoratchisi"
        }
        if instance.role in groups_by_role.keys():
            instance.is_staff = True
            group_name = groups_by_role[instance.role]
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                perms = PermissionsByGroupName[group_name]
                permissions = Permission.objects.filter(codename__in=perms)
                group.permissions.add(permissions)