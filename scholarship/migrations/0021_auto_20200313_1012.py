# Generated by Django 2.2.10 on 2020-03-13 04:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarship', '0020_applied_schlarships_scholarship_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Applied_Schlarships',
            new_name='Applied_Scholarships',
        ),
    ]
