# Generated by Django 2.0 on 2021-01-14 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210114_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='acquisti',
            name='codiceID',
            field=models.CharField(default=123, max_length=100, verbose_name='Codice'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fattura',
            name='codiceID',
            field=models.CharField(default=123, max_length=100, verbose_name='Codice'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dispositivo',
            name='ultima_modifica',
            field=models.DateField(auto_now_add=True, verbose_name='Ultima modifica'),
        ),
        migrations.AlterField(
            model_name='fornitore',
            name='creato',
            field=models.DateField(auto_now_add=True, verbose_name='Data creazione'),
        ),
    ]