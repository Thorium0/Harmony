# Generated by Django 4.1.3 on 2022-12-09 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0010_remove_server_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='server_message',
            name='text',
            field=models.CharField(max_length=400),
        ),
    ]
