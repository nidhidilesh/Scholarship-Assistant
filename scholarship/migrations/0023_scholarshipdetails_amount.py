# Generated by Django 2.2.10 on 2020-03-15 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0022_auto_20200313_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarshipdetails',
            name='amount',
            field=models.CharField(default=1, max_length=5000),
            preserve_default=False,
        ),
    ]
