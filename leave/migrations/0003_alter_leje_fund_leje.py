# Generated by Django 3.2.2 on 2021-05-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_alter_leje_fund_leje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leje',
            name='fund_leje',
            field=models.DateTimeField(),
        ),
    ]