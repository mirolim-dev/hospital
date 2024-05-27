from django import forms
from .models import Staff

class StaffAdminForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'first_name',
            'last_name',
            'phone',
            'address',
            'gender',
            'passport',
            'image',
            'salary',
            'is_working',
            'role',
            'visible_password',
            'description',
        ]