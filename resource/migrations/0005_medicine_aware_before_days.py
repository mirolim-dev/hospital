# Generated by Django 4.2.13 on 2024-05-22 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0004_medicine_aware_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='aware_before_days',
            field=models.PositiveBigIntegerField(default=3, help_text='Dorining yaroqlilik muddati         tugashidan necha kun avval ogohlantirlishi kerakligini kiriting', verbose_name='Kun avval ogohlantir'),
        ),
    ]
