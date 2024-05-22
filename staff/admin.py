from django.contrib import admin

from .models import Staff
from .forms import StaffAdminForm
# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ['first_name', 'last_name', 'phone', 'address', 'role', 'is_working']
    search_fields = ['first_name', 'last_name', 'phone']
    list_filter = ['role', 'is_working']
admin.site.register(Staff, StaffAdmin)