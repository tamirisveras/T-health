# Generated by Django 5.1.1 on 2024-09-09 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkAgenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agenda', models.IntegerField(blank=True, verbose_name='id_agenda')),
                ('author', models.IntegerField(blank=True, verbose_name='id_user')),
            ],
        ),
    ]
