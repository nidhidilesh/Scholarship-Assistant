# Generated by Django 2.2.10 on 2020-03-17 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0027_personal_info_family_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal_info',
            name='category',
            field=models.CharField(max_length=200, null=True),
        ),
    ]