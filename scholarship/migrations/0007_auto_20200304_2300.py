# Generated by Django 2.2.10 on 2020-03-04 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0006_auto_20200304_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarshipdetails',
            name='income',
            field=models.FloatField(),
        ),
    ]