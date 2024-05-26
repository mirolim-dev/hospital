from django.db import models
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from config.variables import MEASURE
from staff.models import Staff
from .validators import (
    validate_invalid_stuff_amount,
    validate_invalid_medicine_amount,
)


# Create your models here.
class Room(models.Model):
    class Meta:
        verbose_name = _('Xona')
        verbose_name_plural = _('Xonalar')
    name = models.CharField(max_length=60, unique=True, verbose_name=_("Nomi"))

    def __str__(self) -> str:
        return self.name

    def get_all_invalid_stuffs(self):
        return self.invalidstuff_set.select_related('room', 'stuff')

    def get_all_active_stuffs(self):
        return self.roomstuff_set.filter(amount__gt=0).values("stuff")


class Stuff(models.Model):
    class Meta:
        verbose_name = _('Jihoz')
        verbose_name_plural = _('Jihozlar')
    name = models.CharField(max_length=60, unique=True, verbose_name=_("Nomi"))
    image = models.ImageField(upload_to="Stuff/", blank=True, verbose_name=_("rasm"))
    description = models.TextField(verbose_name=_("Izoh"), help_text=_("bu yerga mahsulotning harakteristikasini yozilishi kerak"))

    def __str__(self):
        return self.name


class RoomStuff(models.Model):
    class Meta:
        verbose_name = _("Xona jihozi")
        verbose_name_plural = _("Xona jihozlari")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Xona"))
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name=_("Jihoz"))
    amount = models.PositiveBigIntegerField(default=1, verbose_name=_("Miqdor"))
    
    def __str__(self):
        return f"{self.room.name} | {self.stuff.name}"
    

class InvalidStuff(models.Model):
    class Meta:
        verbose_name = _("Yaroqsiz Jihoz")
        verbose_name_plural = _("Yaroqsiz Jihozlar")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Xona"))
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name=_("Jihoz"))
    amount = models.PositiveBigIntegerField(default=1, verbose_name=_("Miqdori"))
    description = models.TextField(verbose_name="Izoh", help_text=_("Yaroqsizga chiqarish sababi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaroqsizga chiqarilgan vaqt"))

    def __str__(self):
        return f"{self.room.name} | {self.stuff.name} | {self.amount}"

    def clean(self) -> None:
        super().clean()
        # validate_invalid_room_and_stuff(self.room, self.stuff)
        validate_invalid_stuff_amount(self.room, self.stuff, self.amount)


class Medicine(models.Model):
    class Meta:
        verbose_name = _("Dori vositasi")
        verbose_name_plural = _("Dori vositalari")
    name = models.CharField(max_length=150, verbose_name=_("nomi"))
    measure = models.CharField(max_length=5, choices=MEASURE().choices, default=MEASURE().GRAMM, verbose_name=_("O'lchov birligi"))
    aware_amount = models.DecimalField(max_digits=15, decimal_places=2, default=100, verbose_name=_("Ogohlantirish miqdori"))
    aware_before_days = models.PositiveBigIntegerField(default=3, verbose_name=_("Kun avval ogohlantir"), help_text=_("Dorining yaroqlilik muddati tugashidan necha kun avval ogohlantirlishi kerakligini kiriting"))
    description = models.TextField(verbose_name=_("Dori xususiyati"), null=True)
    def __str__(self):
        return self.name + '|' + self.get_measure_display()

    @admin.display(description=_('Barcha miqdor'))
    def get_total_available_amount(self):
        # measure_instance = MEASURE()

        # # Calculate conversion factor to the medicine's measure unit
        # conversion_factor = measure_instance.values[self.measure]

        # # Use annotation to calculate the available amount in the medicine's measure unit
        # total_available = BatchMedicine.objects.filter(medicine=self, status=1).annotate(
        #     available_amount_converted=ExpressionWrapper(
        #         F('available_amount') * measure_instance.convert(F('measure'), self.measure)),
        #         output_field=DecimalField()
        #     ).aggregate(total=Sum('available_amount_converted'))['total']
        # return total_available if total_available else Decimal('0')
        pass

class BatchMedicine(models.Model):
    class Meta:
        verbose_name = _("Dori Partiyasi")
        verbose_name_plural = _("Dorilar Partiyalari")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name=_("Dori"))
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=1, verbose_name=_("miqdor"))
    available_amount = models.DecimalField(max_digits=15, decimal_places=2, default=1, verbose_name=_("mavjud miqdori"))
    measure = models.CharField(max_length=5, choices=MEASURE().choices, default=MEASURE().GRAMM, verbose_name=_("Miqdor o'lchovi"))
    available_measure = models.CharField(max_length=5, choices=MEASURE().choices, default=MEASURE().GRAMM, verbose_name=_("Mavjud miqdor o'lchovi"))
    available_till = models.DateField(verbose_name=_("Yaroqlilik muddati"))
    STATUS_CHOICES = (
        (0, _("Yaroqlilik muddati tugagan")),
        (1, _("Active")),
        (2, _("Tugatilgan"))
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name=_("Xolati"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Keltirilgan vaqt"), null=True)

    def __str__(self):
        return f"ID: {self.pk} | {BatchMedicine._meta.verbose_name} | {self.medicine.name}"

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.available_amount = self.amount
            self.available_measure = self.measure
        super(BatchMedicine, self).save(*args, **kwargs)


class MedicineUsage(models.Model):
    class Meta:
        verbose_name = _("Foydalanilgan dori")
        verbose_name_plural = _("Foydalanilgan dorilar")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name=_("Dori"))
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, verbose_name=_("Xodim"))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("miqdor"), default=1)
    measure = models.CharField(max_length=5, choices=MEASURE().choices, default=MEASURE().GRAMM, verbose_name=_("O'lchov birligi"))
    description = models.TextField(verbose_name=_("Izoh"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Foydalanigan vaqti"))

    def __str__(self):
        return f"{MedicineUsage._meta.verbose_name} | {self.medicine.name} | {self.get_measure_display()}"
    

class InvalidMedicine(models.Model):
    class Meta:
        verbose_name = _("Yaroqsiz dori")
        verbose_name_plural = _("Yaroqsiz dorilar")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, verbose_name=_("Dori"))
    batch = models.ForeignKey(BatchMedicine, on_delete=models.CASCADE, verbose_name=_("Partiya"))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Miqdor"), null=True)
    measure = models.CharField(max_length=5, choices=MEASURE().choices, default=MEASURE().GRAMM, verbose_name=_("O'lchov birligi"))
    reason = models.TextField(verbose_name=_("Sababi"))
    tracked_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qayd etilgan vaqt"))

    def __str__(self)->str:
        return f"{BatchMedicine._meta.verbose_name}-{self.batch.id} | {self.batch.medicine.name}"
    
    def clean(self) -> None:
        super().clean()
        validate_invalid_medicine_amount(self.batch, self.amount, self.measure)


