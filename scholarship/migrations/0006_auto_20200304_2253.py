# Generated by Django 2.2.10 on 2020-03-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0005_scholarshipdetails_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarshipdetails',
            name='helpline',
            field=models.BigIntegerField(),
        ),
    ]
