# Generated by Django 4.2.13 on 2024-05-22 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0006_batchmedicine'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchmedicine',
            name='measure',
            field=models.CharField(choices=[('g', 'Gramm'), ('mg', 'MilliGramm'), ('l', 'Liter'), ('ml', 'MilliLiter'), ('unit', 'Dona')], default='g', max_length=5, verbose_name="O'lchov birligi"),
        ),
    ]
