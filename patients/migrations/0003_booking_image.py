# Generated by Django 3.2 on 2021-06-26 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_alter_chatroom_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='image',
            field=models.ImageField(default=1, upload_to='media/'),
            preserve_default=False,
        ),
    ]
