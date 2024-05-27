from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Staff, CustomUser
from account.models import CustomUser  # Adjust the import according to your app structure

class StaffSignalTest(TestCase):
    
    def setUp(self):
        # Create necessary content type for the Permission
        content_type = ContentType.objects.create(
            app_label='staff',
            model='Staff',  # replace 'mymodel' with an actual model name from your app
        )
        
        # Create necessary permissions for testing
        self.permission = Permission.objects.create(
            codename='add_kirim',
            name='Can add Kirim',
            content_type=content_type
        )
        
        # Define your permissions by group name
        global PermissionsByGroupName
        PermissionsByGroupName = {
            "Mudir": ['add_kirim'],
            "Katta hamshira": ['add_kirim'],
            "Resurs nazoratchisi": ['add_kirim'],
        }
    
    def test_staff_creation_adds_correct_group(self):
        staff = Staff.objects.create(username='testuser1', phone='458712554', role=2)  # Assuming role 2 is 'Katta hamshira'
        self.assertTrue(staff.groups.filter(name="Katta hamshira").exists()) 

    def test_staff_creation_adds_correct_group(self):
        # Create a staff instance with role "Mudir"
        staff = Staff.objects.create(
            phone="+998900000000",
            username="testuser",
            first_name="Test",
            last_name="User",
            role=1,  # Mudir
        )
        
        # Check if the group "Mudir" was created and assigned
        mudir_group = Group.objects.get(name="Mudir")
        self.assertIn(mudir_group, staff.groups.all())
        self.assertTrue(staff.groups.filter(name="Mudir").exists())

    def test_staff_update_changes_group(self):
        staff = Staff.objects.create(username='testuser2', phone='15478521', role=2)  # Assuming role 2 is 'Katta hamshira'
        self.assertTrue(staff.groups.filter(name="Katta hamshira").exists())
        
        # Update the role and check group change
        staff.role = 1  # Assuming role 1 is 'Mudir'
        staff.save()

        katta_hamshira_group = Group.objects.get(name="Katta hamshira")
        self.assertFalse(staff.groups.filter(name="Katta hamshira").exists())
        self.assertTrue(staff.groups.filter(name="Mudir").exists())

    def test_staff_creation_does_not_add_non_existent_group(self):
        # Create a staff instance with role "Doctor" which does not have a group mapping
        staff = Staff.objects.create(
            phone="+998900000002",
            username="testuser2",
            first_name="Test2",
            last_name="User2",
            role=3,  # Doctor
        )

        # Check if no group was assigned
        self.assertEqual(staff.groups.count(), 0)

    def test_staff_creation_adds_correct_group_and_sets_is_staff(self):
        staff = Staff.objects.create(username='testuser1', phone='458712554', role=2)  # Assuming role 2 is 'Katta hamshira'
        self.assertTrue(staff.groups.filter(name="Katta hamshira").exists())
        self.assertTrue(staff.is_staff)  # Ensure is_staff is True

    def test_staff_creation_adds_correct_group_and_sets_is_staff(self):
        # Create a staff instance with role "Mudir"
        staff = Staff.objects.create(
            phone="+998900000000",
            username="testuser",
            first_name="Test",
            last_name="User",
            role=1,  # Mudir
        )
        
        # Check if the group "Mudir" was created and assigned
        mudir_group = Group.objects.get(name="Mudir")
        self.assertIn(mudir_group, staff.groups.all())
        self.assertTrue(staff.groups.filter(name="Mudir").exists())
        self.assertTrue(staff.is_staff)  # Ensure is_staff is True

    def test_staff_update_changes_group_and_sets_is_staff(self):
        staff = Staff.objects.create(username='testuser2', phone='15478521', role=2)  # Assuming role 2 is 'Katta hamshira'
        self.assertTrue(staff.groups.filter(name="Katta hamshira").exists())
        self.assertTrue(staff.is_staff)  # Ensure is_staff is True
        
        # Update the role and check group change
        staff.role = 1  # Assuming role 1 is 'Mudir'
        staff.save()

        katta_hamshira_group = Group.objects.get(name="Katta hamshira")
        self.assertFalse(staff.groups.filter(name="Katta hamshira").exists())
        self.assertTrue(staff.groups.filter(name="Mudir").exists())
        self.assertTrue(staff.is_staff)  # Ensure is_staff is still True

    def test_staff_creation_does_not_add_non_existent_group_and_sets_is_staff(self):
        # Create a staff instance with role "Doctor" which does not have a group mapping
        staff = Staff.objects.create(
            phone="+998900000002",
            username="testuser2",
            first_name="Test2",
            last_name="User2",
            role=3,  # Doctor
        )

        # Check if no group was assigned
        self.assertEqual(staff.groups.count(), 0)
        self.assertFalse(staff.is_staff)  # Ensure is_staff is False

    def test_staff_update_to_non_staff_role_unsets_is_staff(self):
        staff = Staff.objects.create(username='testuser3', phone='15478523', role=2)  # Assuming role 2 is 'Katta hamshira'
        self.assertTrue(staff.groups.filter(name="Katta hamshira").exists())
        self.assertTrue(staff.is_staff)  # Ensure is_staff is True

        # Update the role to one without a group
        staff.role = 3  # Assuming role 3 is 'Doctor' which doesn't have a group
        staff.save()

        self.assertEqual(staff.groups.count(), 0)
        self.assertFalse(staff.is_staff)  # Ensure is_staff is False