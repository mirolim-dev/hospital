from django.db import models

from config.variables import MEASURE
from .validators import validate_invalid_stuff_amount

# Create your models here.
class Room(models.Model):
    class Meta:
        verbose_name = 'Xona'
        verbose_name_plural = 'Xonalar'
    name = models.CharField(max_length=60, unique=True, verbose_name="Nomi")

    def __str__(self) -> str:
        return self.name

    def get_all_invalid_stuffs(self):
        return self.invalidstuff_set.select_related('room', 'stuff')

    def get_all_active_stuffs(self):
        return self.roomstuff_set.filter(amount__gt=0).values("stuff")


class Stuff(models.Model):
    class Meta:
        verbose_name = 'Jihoz'
        verbose_name_plural = 'Jihozlar'
    name = models.CharField(max_length=60, unique=True, verbose_name="Nomi")
    image = models.ImageField(upload_to="Stuff/", blank=True)
    description = models.TextField(verbose_name="Izoh", help_text="bu yerga mahsulotning harakteristikasini yozilishi kerak")

    def __str__(self):
        return self.name


class RoomStuff(models.Model):
    class Meta:
        verbose_name = "Xona jihozi"
        verbose_name_plural = "Xona jihozlari"
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Xona")
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name="Jihoz")
    amount = models.PositiveBigIntegerField(default=1, verbose_name="Miqdor")
    
    def __str__(self):
        return f"{self.room.name} | {self.stuff.name}"
    

class InvalidStuff(models.Model):
    class Meta:
        verbose_name = "Yaroqsiz Jihoz"
        verbose_name_plural = "Yaroqsiz Jihozlar"
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Xona")
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name="Jihoz")
    amount = models.PositiveBigIntegerField(default=1, verbose_name="Miqdori")
    description = models.TextField(verbose_name="Izoh", help_text="Yaroqsizga chiqarish sababi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaroqsizga chiqarilgan vaqt")

    def __str__(self):
        return f"{self.room.name} | {self.stuff.name} | {self.amount}"

    def clean(self) -> None:
        super().clean()
        # validate_invalid_room_and_stuff(self.room, self.stuff)
        validate_invalid_stuff_amount(self.room, self.stuff, self.amount)


class Medicine(models.Model):
    class Meta:
        verbose_name = "Dori vositasi"
        verbose_name_plural = "Dori vositalari"
    name = models.CharField(max_length=150, verbose_name="nomi")
    measure = models.CharField(max_length=5, choices=MEASURE().choices, default=MEASURE().GRAMM, verbose_name="O'lchov birligi")
    aware_amount = models.DecimalField(max_digits=15, decimal_places=2, default=100, verbose_name="Ogohlantirish miqdori")
    aware_before_days = models.PositiveBigIntegerField(default=3, verbose_name="Kun avval ogohlantir", help_text="Dorining yaroqlilik muddati \
        tugashidan necha kun avval ogohlantirlishi kerakligini kiriting")
    def __str__(self):
        return self.name + '|' + self.get_measure_display()

    
    def get_available_amount(self):
        pass
    

class BatchMedicine(models.Model):
    class Meta:
        verbose_name = "Dori Partiyasi"
        verbose_name_plural = "Dorilar Partiyalari"
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name="Dori")
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=1, verbose_name="miqdor")
    available_till = models.DateField(verbose_name="Yaroqlilik muddati")
    STATUS_CHOICES = (
        (0, "Yaroqlilik muddati tugagan"),
        (1, "Active"),
        (2, "Tugatilgan")
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Xolati")

    def __str__(self):
        return f"Partiya{self.id}|{self.medicine.name} | {self.amount}"
    
    def get_available_amount(self):
        pass