# Generated by Django 4.2.13 on 2024-05-26 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Ayol'), (1, 'Erkak')], default=1, verbose_name='Jinsi'),
        ),
    ]