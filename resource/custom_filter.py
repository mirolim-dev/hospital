from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.admin import SimpleListFilter

class FilterBatchMedicineByCreatedAtTime(SimpleListFilter):
    title = "Keltirilgan vaqt bo'yicha filterlash"
    parameter_name = 'time_filter'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Bugun'),
            ('yesterday', 'Kecha'),
            ('weekly', 'Hafta davomida'),
            ('monthly', 'Oy davomida'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            today = now().date()
            return queryset.filter(created_at__date=today)
        elif self.value() == 'yesterday':
            yesterday = now().date() - timedelta(days=1)
            return queryset.filter(created_at__date=yesterday)
        elif self.value() == 'weekly':
            today = now()
            start_of_week = today - timedelta(days=today.weekday())
            return queryset.filter(created_at__date__gte=start_of_week.date())
        elif self.value() == 'monthly':
            today = now()
            start_of_month = today.replace(day=1)
            return queryset.filter(created_at__date__gte=start_of_month.date())
        return queryset