from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import CustomUser
from .utils import generate_password
from .validators import validate_file
# Create your models here.
class Staff(CustomUser):
    class Meta:
        verbose_name = _("Xodim")
        verbose_name_plural = _("Xodimlar")
    passport = models.FileField(upload_to="Staff/passport", verbose_name=_("Passport nusxasi"))
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=_("Maosh"), help_text=_("UZS da kiritilsin"))
    image = models.ImageField(upload_to="Staff/image3x4", verbose_name=_("rasm"), help_text=_("3X4 rasm yuklansin"))
    ROLE_CHOICES = (
        (1, _("Mudir")),
        (2, _("Katta hamshira")),
        (3, _("Doctor")),
        (4, _("Hamshira")),
        (5, _("Farrosh")),
        (6, _("Qorovul")),
        (7, _("Haydovchi")),
        (8, _("Resurs nazoratchisi")),
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=3, verbose_name=_("Hodim turi"))
    is_working = models.BooleanField(default=True, verbose_name=_("Ishlayotganlik statusi"))
    description = models.TextField(verbose_name=_("Izoh"), help_text=_("Qo'shimcha izohlar uchun. Hodim nima ish qilishi va ho kazo larni kiritsa bo'ladi"))
    visible_password = models.CharField(max_length=150, null=True, verbose_name=_("Parol"), blank=True)

    def __str__(self):
        return self.get_full_name()

    def clean(self) -> None:
        super().clean()
        validate_file(file=self.passport, allowed_types=['.pdf', '.docx', '.png', '.jpg', '.doc'], max_size=2)
        validate_file(file=self.image, allowed_types=['.png', '.jpg'], max_size=2)

    def save(self, *args, **kwargs):
        if not self.visible_password:
            self.visible_password = generate_password(8)
        self.set_password(self.visible_password)
        return super().save(*args, **kwargs)

    def display_role(self):
        return self.ROLE_CHOICES[self.role-1][1]

class Attandace(models.Model):
    class Meta:
        verbose_name = _('Davomat')
        verbose_name_plural = _("Davomatlar")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name=_("Xodim"))
    tracked_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qayd etilgan vaqt"))

    def __str__(self):
        return f"{_('Davomat')} | {self.staff}"
    
