# Generated by Django 2.0 on 2021-02-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistenza', '0006_verifica_dataverifica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifica',
            name='cei',
            field=models.ManyToManyField(blank=True, related_name='has_verifica', to='assistenza.normativaCodice'),
        ),
        migrations.AlterField(
            model_name='verifica',
            name='dataVerifica',
            field=models.DateField(blank=True, null=True, verbose_name='Data verifica'),
        ),
    ]
