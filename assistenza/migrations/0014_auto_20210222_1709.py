# Generated by Django 2.0 on 2021-02-22 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistenza', '0013_auto_20210222_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifica',
            name='ceiMultiple',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]
