# Generated by Django 4.0.1 on 2022-11-02 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_remove_message_receiver_conversation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]