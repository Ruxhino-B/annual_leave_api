# Generated by Django 3.2.2 on 2021-05-23 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_rename_user_id_employee_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='user',
            new_name='user_id',
        ),
    ]
