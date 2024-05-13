from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import InvalidStuff, RoomStuff

@receiver(post_save, sender=InvalidStuff)
def update_roomstuff_amount(sender, instance, **kwargs):
    room_stuff = RoomStuff.objects.get(room=instance.room, stuff=instance.stuff)
    room_stuff.amount -= instance.amount
    room_stuff.save()