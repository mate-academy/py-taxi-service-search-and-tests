# Generated by Django 4.0.2 on 2023-03-28 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='driver',
            options={'ordering': ['last_name'], 'verbose_name': 'driver', 'verbose_name_plural': 'drivers'},
        ),
    ]
