# Generated by Django 2.2.10 on 2020-03-17 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0028_personal_info_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal_info',
            name='highest_qualification',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
