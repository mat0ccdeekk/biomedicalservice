# Generated by Django 2.0 on 2021-02-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistenza', '0012_auto_20210222_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifica',
            name='richiestaFile',
            field=models.FileField(blank=True, default=True, null=True, upload_to='Richiesta_Verifica/%Y/%m/%d', verbose_name='Richiesta'),
        ),
    ]
