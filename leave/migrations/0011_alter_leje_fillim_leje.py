# Generated by Django 3.2.2 on 2021-06-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0010_alter_approvimleje_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leje',
            name='fillim_leje',
            field=models.DateTimeField(),
        ),
    ]
