# Generated by Django 2.2 on 2019-12-20 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prac_app', '0004_remove_like_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='prac_app.User'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
