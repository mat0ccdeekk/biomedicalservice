# Generated by Django 2.0 on 2021-01-13 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AltriFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='pdf_gare_/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='GaraPubblica',
            fields=[
                ('idGara', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('ente', models.CharField(max_length=100)),
                ('scadenza', models.DateField()),
                ('oggetto', models.CharField(max_length=100)),
                ('bando', models.FileField(blank=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Gara Pubblica',
                'verbose_name_plural': 'Gare Pubbliche',
            },
        ),
        migrations.AddField(
            model_name='altrifile',
            name='gara',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gare.GaraPubblica'),
        ),
    ]
