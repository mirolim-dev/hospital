from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from config.variables import MEASURE


measure_instance = MEASURE()
# def validate_invalid_room_and_stuff(room:object, stuff:object):
#     print(room.get_all_active_stuffs(), stuff)
#     if stuff not in room.get_all_active_stuffs():
#         error_message = f"{room.name} xonasida {stuff.name} jihoz mavjud emas"
#         raise ValidationError(error_message)

def validate_invalid_stuff_amount(room:object, stuff:object, amount:int):
    room_stuff = room.roomstuff_set.get(stuff=stuff)
    if room_stuff.amount < amount:
        error_message = _("Xonada siz ko'rsatgan miqdordagi jihoz mavjud emas")
        raise ValidationError(error_message)


def validate_medicine_usage_amount(medicine:object, amount, measure):
    pass

 
def validate_invalid_medicine_amount(batch:object, amount:Decimal, measure:str):
    try:
        if amount == 0:
            raise ValidationError(_("Kiritayotgan miqdoringiz 0 bo'lishi mumkun emas"))
        convertion_difference = measure_instance.convert(batch.available_measure, measure)
        substraction_amount = (batch.available_amount*convertion_difference) - (amount*convertion_difference)
        if substraction_amount < 0:
            error_message = _("Ushbu partiyada kiritilgan miqdordagi {medicine_name} mavjud emas. \
                Ushbu partiyada qolgan miqdor {amount} {measure}").format(medicine_name=batch.medicine.name, \
                    amount=batch.available_amount, measure=batch.available_measure)
            raise ValidationError(error_message)
    except ValueError as e:
        raise ValidationError(e)