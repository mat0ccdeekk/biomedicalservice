# Generated by Django 2.0 on 2021-01-15 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210115_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisti',
            name='stato',
            field=models.CharField(blank=True, choices=[('ordinato', 'Ordinato'), ('spedito', 'Spedito'), ('completo', 'Completo')], max_length=20),
        ),
    ]