# Generated by Django 3.1.6 on 2022-04-08 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Address'},
        ),
    ]
