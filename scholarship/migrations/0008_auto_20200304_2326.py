# Generated by Django 2.2.10 on 2020-03-04 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0007_auto_20200304_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarshipdetails',
            name='helpline',
            field=models.CharField(max_length=200),
        ),
    ]