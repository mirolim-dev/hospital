# Generated by Django 4.2.13 on 2024-05-22 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0002_medicine_alter_invalidstuff_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='measure',
            field=models.CharField(choices=[('g', 'Gramm'), ('mg', 'MilliGramm'), ('l', 'Liter'), ('ml', 'MilliLiter'), ('unit', 'Dona')], default='g', max_length=5, verbose_name="O'lchov birligi"),
        ),
    ]
