# Generated by Django 2.0 on 2021-02-12 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistenza', '0003_auto_20210212_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verifica',
            name='cei',
        ),
        migrations.AddField(
            model_name='verifica',
            name='cei',
            field=models.ManyToManyField(to='assistenza.normativaCodice'),
        ),
    ]
