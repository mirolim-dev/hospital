from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

# Define the permissions for each group
PermissionsByGroupName = {
    "Mudir": [
        'add_income', 'view_income', 'add_outlay', 'view_outlay',
        'add_batchmedicine', 'view_batchmedicine',
        'delete_invalidmedicine', 'view_invalidmedicine',
        'delete_invalidstuff', 'view_invalidstuff', 'add_medicine',
        'change_medicine', 'view_medicine', 'change_medicineusage',
        'delete_medicineusage', 'view_medicineusage', 'add_room',
        'change_room', 'view_room', 'delete_roomstuff', 'view_roomstuff',
        'add_stuff', 'change_stuff', 'delete_stuff', 'view_stuff',
        'view_attandace', 'add_staff', 'change_staff', 'view_staff',
    ],
    "Katta hamshira": [
       'add_income', 'view_income', 'add_outlay', 'view_outlay', 
       'view_batchmedicine', 'view_invalidmedicine',
       'add_invalidstuff', 'view_invalidstuff', 'add_medicine',
       'view_medicine', 'view_medicineusage', 'add_room',
       'change_room', 'view_room', 'add_roomstuff',
       'view_roomstuff', 'add_stuff', 'view_stuff',
       'add_attandace', 'view_attandace', 'add_staff',
       'view_staff',
    ],
    "Resurs nazoratchisi": [
       'add_batchmedicine', 'view_batchmedicine',
       'add_invalidmedicine', 'view_invalidmedicine',
       'add_invalidstuff', 'view_invalidstuff',
       'add_medicine', 'view_medicine', 'add_medicineusage',
       'view_medicineusage', 'add_room', 'view_room',
       'add_roomstuff', 'view_roomstuff', 'add_stuff',
       'view_stuff',
    ],
}

class Command(BaseCommand):
    help = "Activates predefined permissions for groups"

    def handle(self, *args, **kwargs):
        for group_name, perm_codes in PermissionsByGroupName.items():
            group, created = Group.objects.get_or_create(name=group_name)

            # Fetch only existing permissions
            permissions = Permission.objects.filter(
                Q(codename__in=perm_codes)
            )

            # Assign permissions
            group.permissions.set(permissions)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            self.stdout.write(self.style.SUCCESS(f"Updated permissions for: {group_name}"))

        self.stdout.write(self.style.SUCCESS("Permission activation completed successfully!"))
