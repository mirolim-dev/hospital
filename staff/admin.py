from django.contrib import admin

from .models import Staff, Attandace
from .forms import StaffAdminForm
from .custom_filers import FilterAttandanceByTime
# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ['first_name', 'last_name', 'phone', 'address', 'role', 'is_working']
    search_fields = ['first_name', 'last_name', 'phone']
    list_filter = ['role', 'is_working']
admin.site.register(Staff, StaffAdmin)


class AttandanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'get_staff_role', 'tracked_at']
    search_fields = ['staff__first_name', 'staff__last_name']
    list_filter = ['staff__role', FilterAttandanceByTime]

    def get_staff_role(self, obj):
        staff_id = obj.staff_id
        return Staff.objects.get(pk=staff_id).display_role()
    get_staff_role.short_description = 'Xodim turi'

admin.site.register(Attandace, AttandanceAdmin)
    