# Generated by Django 2.2.10 on 2020-03-31 10:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0033_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]