from django.db.models.signals import post_save
from django.dispatch import receiver

from config.variables import MEASURE
from .models import (
    InvalidStuff, RoomStuff, 
    MedicineUsage, Medicine, BatchMedicine,
    )

@receiver(post_save, sender=InvalidStuff)
def update_roomstuff_amount(sender, instance, **kwargs):
    room_stuff = RoomStuff.objects.get(room=instance.room, stuff=instance.stuff)
    room_stuff.amount -= instance.amount
    room_stuff.save()


@receiver(post_save, sender=MedicineUsage)
def update_batch_medicine_amount(sender, instance, **kwargs):
    medicine = instance.medicine
    measure_instance = MEASURE()
    amount = instance.amount
    measure = instance.measure
    
    def get_last_batch_medicine(medicine):
        return medicine.batchmedicine_set.filter(status=1).last()

    def get_batch_medicine_amount_value(batch_medicine):
        return batch_medicine.available_amount * measure_instance.values[batch_medicine.available_measure]

    def update_batch(batch, amount_difference, status=None):
        batch.available_amount = amount_difference / measure_instance.values[batch.available_measure]
        if status:
            batch.status = status
        batch.save()
    batch_medicine = get_last_batch_medicine(medicine)
    difference_amount_value = get_batch_medicine_amount_value(batch_medicine) - (amount*measure_instance.values[measure])

    def manage_condition(difference_amount_value, batch_medicine):
        if difference_amount_value > 0:
            update_batch(batch_medicine, difference_amount_value)
        elif difference_amount_value < 0:
            update_batch(batch_medicine, 0, 2)
            batch_medicine.save()
            batch_medicine = get_last_batch_medicine(medicine)
            difference_amount_value = batch_medicine.available_amount + difference_amount_value
            manage_condition(difference_amount_value, batch_medicine)
        elif difference_amount_value == 0:
            update_batch(batch_medicine, 0, 2)
            batch_medicine.status = 2
            batch_medicine.save()
    manage_condition(difference_amount_value, batch_medicine)