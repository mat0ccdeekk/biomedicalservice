# Generated by Django 2.0 on 2021-02-12 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistenza', '0004_auto_20210212_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prodotti',
            options={'verbose_name': 'Strumento', 'verbose_name_plural': 'Strumenti'},
        ),
        migrations.AlterField(
            model_name='verifica',
            name='prodotti',
            field=models.ManyToManyField(blank=True, related_name='verifica_related', to='assistenza.Prodotti', verbose_name='Strumenti'),
        ),
    ]