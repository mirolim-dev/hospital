from django.contrib import admin
from django.utils import timezone

from .models import Staff, Attandace
from .forms import StaffAdminForm
from .custom_filers import FilterAttandanceByTime
# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ['first_name', 'last_name', 'phone', 'address', 'role', 'is_working']
    search_fields = ['first_name', 'last_name', 'phone']
    list_filter = ['role', 'is_working']
    list_per_page = 20
admin.site.register(Staff, StaffAdmin)


class AttandanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'get_staff_role', 'tracked_at']
    search_fields = ['staff__first_name', 'staff__last_name']
    list_filter = ['staff__role', FilterAttandanceByTime]
    list_per_page = 20

    def get_staff_role(self, obj):
        staff_id = obj.staff_id
        return Staff.objects.get(pk=staff_id).display_role()
    get_staff_role.short_description = 'Xodim turi'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "staff":
            # Get today's date
            today = timezone.now().date()
            # Get all staff who have been tracked today
            tracked_staff_ids = Attandace.objects.filter(tracked_at__date=today).values_list('staff_id', flat=True)
            # Exclude the staff who have been tracked today from the queryset
            kwargs["queryset"] = Staff.objects.exclude(id__in=tracked_staff_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Attandace, AttandanceAdmin)
    