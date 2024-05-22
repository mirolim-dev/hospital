from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    InvalidStuff, RoomStuff, 
    MedicineUsage, Medicine, BatchMedicine,
    )

@receiver(post_save, sender=InvalidStuff)
def update_roomstuff_amount(sender, instance, **kwargs):
    room_stuff = RoomStuff.objects.get(room=instance.room, stuff=instance.stuff)
    room_stuff.amount -= instance.amount
    room_stuff.save()


# @receiver(post_save, sender=MedicineUsage)
# def update_batch_medicine_amount(sender, instance, **kwargs):
#     medicine = instance.medicine
#     amount = instance.amount
#     measure = instance.measure