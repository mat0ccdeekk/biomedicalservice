# Generated by Django 2.0 on 2021-01-15 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20210115_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisti',
            name='ordinato',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ordinato'),
        ),
    ]