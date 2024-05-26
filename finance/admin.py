from django.contrib import admin

from  .models import Income, Outlay

# Register your models here.

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'created_at']
    search_fields = ['name']
    list_per_page = 20
admin.site.register(Income, IncomeAdmin)


class OutlayAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'created_at']
    search_fields = ['name']
    list_per_page = 20
admin.site.register(Outlay, OutlayAdmin)