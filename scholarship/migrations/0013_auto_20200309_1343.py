# Generated by Django 2.2.10 on 2020-03-09 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0012_scholarshipdetails_updated_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarshipdetails',
            name='updated_helpline',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='scholarshipdetails',
            name='updated_name',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
