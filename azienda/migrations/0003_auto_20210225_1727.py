# Generated by Django 2.0 on 2021-02-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azienda', '0002_auto_20210224_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]