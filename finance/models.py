from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Income(models.Model):
    class Meta:
        verbose_name = _("Kirim")
        verbose_name_plural = _("Kirimlar")
    name = models.CharField(max_length=100, verbose_name=_("nomi"))
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("miqdori"), help_text=_("UZS da kiritilsin"))
    description = models.TextField(verbose_name=_("Izoh"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("qayd etilgan vaqt"))

    def __str__(self)->str:
        return self.name


class Outlay(models.Model):
    class Meta:
        verbose_name = _("Chiqim")
        verbose_name_plural = _("Chiqimlar")
    name = models.CharField(max_length=100, verbose_name=_("nomi"))
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("miqdori"), help_text=_("UZS da kiritilsin"))
    description = models.TextField(verbose_name=_("Izoh"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("qayd etilgan vaqt"))
    
    def __str__(self)->str:
        return self.name
