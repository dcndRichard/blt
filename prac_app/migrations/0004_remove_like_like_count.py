# Generated by Django 2.2 on 2019-12-20 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prac_app', '0003_wish_granted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='like_count',
        ),
    ]
