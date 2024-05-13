from django.core.exceptions import ValidationError

def validate_invalid_room_and_stuff(room:object, stuff:object):
    if stuff not in room.get_all_active_staffs():
        error_message = f"{room.name} xonasida {stuff.name} jihoz mavjud emas"
        raise ValidationError(error_message)

def validate_invalid_stuff_amount(room:object, stuff:object, amount:int):
    room_stuff = room.roomstuff_set.get(stuff=stuff)
    if room_stuff.amount < amount:
        error_message = f"Xonada siz ko'rsatgan miqdordagi jihoz mavjud emas"
        raise ValidationError(error_message)