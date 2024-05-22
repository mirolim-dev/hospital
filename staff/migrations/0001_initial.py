# Generated by Django 4.2.13 on 2024-05-22 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('passport', models.FileField(upload_to='Staff/passport', verbose_name='Passport nusxasi')),
                ('salary', models.DecimalField(decimal_places=2, default=0, help_text='UZS da kiritilsin', max_digits=15, verbose_name='Maosh')),
                ('image', models.ImageField(help_text='3X4 rasm yuklansin', upload_to='Staff/image3x4', verbose_name='rasm')),
                ('role', models.IntegerField(choices=[(1, 'Mudir'), (2, 'Katta hamshira'), (3, 'Doctor'), (4, 'Hamshira'), (5, 'Farrosh'), (6, 'Qorovul'), (7, 'Haydovchi'), (8, 'Resurs nazoratchisi')], default=3, verbose_name='Hodim turi')),
                ('is_working', models.BooleanField(default=True, verbose_name='Ishlayotganlik statusi')),
                ('description', models.TextField(help_text="Qo'shimcha izohlar uchun. Hodim nima ish qilishi va ho kazo larni kiritsa bo'ladi", verbose_name='Izoh')),
            ],
            options={
                'verbose_name': 'Xodim',
                'verbose_name_plural': 'Xodimlar',
            },
            bases=('account.customuser',),
        ),
    ]
