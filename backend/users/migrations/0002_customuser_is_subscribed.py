# Generated by Django 3.1.14 on 2022-07-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
