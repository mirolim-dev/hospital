from django.contrib import admin


from .models import (
    Room, RoomStuff, Stuff, 
    InvalidStuff, Medicine, 
    BatchMedicine, MedicineUsage,
    InvalidMedicine
    )
from .forms import BatchMedicineAdminForm

from .custom_filter import FilterBatchMedicineByCreatedAtTime
# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
admin.site.register(Room, RoomAdmin)


class StuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
admin.site.register(Stuff, StuffAdmin)


class RoomStuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'stuff', 'amount']
    search_fields = ['id', 'room__name', 'stuff__name']
admin.site.register(RoomStuff, RoomStuffAdmin)


class InvalidStuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'stuff', 'amount', 'created_at']
    search_fields = ['id', 'room__name', 'stuff__name']
admin.site.register(InvalidStuff, InvalidStuffAdmin)


class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'measure', 'aware_amount', 'aware_before_days']
    search_fields = ['name']
    list_filter = ['measure']
admin.site.register(Medicine, MedicineAdmin)


class BatchMedicineAdmin(admin.ModelAdmin):
    form = BatchMedicineAdminForm
    list_display = ['id', 'medicine', 'amount', 'measure', 'available_amount', 'available_measure', 'available_till', 'status', 'created_at']
    search_fields = ['medicine__name']
    list_filter = ['measure', 'status', 'medicine', FilterBatchMedicineByCreatedAtTime]
    readonly_fields = ['status']
admin.site.register(BatchMedicine, BatchMedicineAdmin)


class MedicineUsageAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'staff', 'amount', 'measure', 'created_at']
    search_fields = ['medicine__name']
    list_filter = ['measure', 'medicine', FilterBatchMedicineByCreatedAtTime]
    readonly_fields = ['staff']
admin.site.register(MedicineUsage, MedicineUsageAdmin)


class InvalidMedicineAdmin(admin.ModelAdmin):
    list_display = ['batch', 'amount', 'measure', 'tracked_at']
    search_fields = ['batch__medicine__name']
    list_filter = ['measure']
admin.site.register(InvalidMedicine, InvalidMedicineAdmin)

