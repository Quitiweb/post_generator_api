# Generated by Django 4.2.2 on 2023-08-18 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='title',
            new_name='name',
        ),
    ]