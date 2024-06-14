from django.contrib import admin
from django.utils.timezone import now
from django.db.models import Sum
from .models import Income, Outlay

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'created_at']
    search_fields = ['name']
    list_per_page = 20
    change_list_template = "admin/income_change_list.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        qs = self.get_queryset(request)
        total_income = qs.filter(
            created_at__month=now().month,
            created_at__year=now().year
        ).aggregate(total=Sum('amount'))['total'] or 0
        extra_context['total_income'] = total_income
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Income, IncomeAdmin)

class OutlayAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'created_at']
    search_fields = ['name']
    list_per_page = 20
    change_list_template = "admin/outlay_change_list.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        qs = self.get_queryset(request)
        total_outlay = qs.filter(
            created_at__month=now().month,
            created_at__year=now().year
        ).aggregate(total=Sum('amount'))['total'] or 0
        extra_context['total_outlay'] = total_outlay
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Outlay, OutlayAdmin)