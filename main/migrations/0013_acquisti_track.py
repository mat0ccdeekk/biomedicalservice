# Generated by Django 2.0 on 2021-01-15 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210115_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='acquisti',
            name='track',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]