# Generated by Django 2.0 on 2021-01-15 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20210115_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisti',
            name='DDT',
            field=models.FileField(blank=True, default='file', upload_to='DDT_Acquisti/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='acquisti',
            name='preventivo',
            field=models.FileField(blank=True, default='file', upload_to='Fattura_Acquisti/%Y/%m/%d'),
        ),
    ]