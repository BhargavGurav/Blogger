# Generated by Django 4.0.3 on 2023-02-09 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_blogs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogs',
            name='user',
        ),
        migrations.DeleteModel(
            name='AppUser',
        ),
        migrations.DeleteModel(
            name='Blogs',
        ),
    ]
