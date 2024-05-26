from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class FilterAttandanceByTime(SimpleListFilter):
    title = _("Vaqt bo'yicha filterlash")
    parameter_name = 'time_filter'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Bugun')),
            ('yesterday', _('Kecha')),
            ('weekly', _('Hafta davomida')),
            ('monthly', _('Oy davomida')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            today = now().date()
            return queryset.filter(tracked_at__date=today)
        elif self.value() == 'yesterday':
            yesterday = now().date() - timedelta(days=1)
            return queryset.filter(tracked_at__date=yesterday)
        elif self.value() == 'weekly':
            today = now()
            start_of_week = today - timedelta(days=today.weekday())
            return queryset.filter(tracked_at__date__gte=start_of_week.date())
        elif self.value() == 'monthly':
            today = now()
            start_of_month = today.replace(day=1)
            return queryset.filter(tracked_at__date__gte=start_of_month.date())
        return queryset