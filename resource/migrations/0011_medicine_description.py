# Generated by Django 4.2.13 on 2024-05-22 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0010_batchmedicine_available_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='description',
            field=models.TextField(null=True, verbose_name='Dori xususiyati'),
        ),
    ]
