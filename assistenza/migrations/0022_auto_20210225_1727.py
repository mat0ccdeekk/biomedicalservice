# Generated by Django 2.0 on 2021-02-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistenza', '0021_auto_20210224_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifica',
            name='stato',
            field=models.CharField(blank=True, default='0', max_length=20, null=True),
        ),
    ]
