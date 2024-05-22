from django.db import models

from account.models import CustomUser
from .validators import validate_file
# Create your models here.
class Staff(CustomUser):
    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"
    passport = models.FileField(upload_to="Staff/passport", verbose_name="Passport nusxasi")
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Maosh", help_text="UZS da kiritilsin")
    image = models.ImageField(upload_to="Staff/image3x4", verbose_name="rasm", help_text="3X4 rasm yuklansin")
    ROLE_CHOICES = (
        (1, "Mudir"),
        (2, "Katta hamshira"),
        (3, "Doctor"),
        (4, "Hamshira"),
        (5, "Farrosh"),
        (6, "Qorovul"),
        (7, "Haydovchi"),
        (8, "Resurs nazoratchisi"),
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=3, verbose_name="Hodim turi")
    is_working = models.BooleanField(default=True, verbose_name="Ishlayotganlik statusi")
    description = models.TextField(verbose_name="Izoh", help_text="Qo'shimcha izohlar uchun. Hodim nima ish qilishi va ho kazo larni kiritsa bo'ladi")

    def __str__(self):
        return self.get_full_name()

    def clean(self) -> None:
        super().clean()
        validate_file(file=self.passport, allowed_types=['.pdf', '.docx', '.png', '.jpg', '.doc'], max_size=2)
        validate_file(file=self.image, allowed_types=['.png', '.jpg'], max_size=2)

    def display_role(self):
        return self.ROLE_CHOICES[self.role][1]