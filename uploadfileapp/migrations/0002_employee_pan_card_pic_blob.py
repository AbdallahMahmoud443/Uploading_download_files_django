# Generated by Django 4.2.13 on 2024-08-03 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadfileapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='pan_card_pic_blob',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
