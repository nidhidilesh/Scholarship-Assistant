# Generated by Django 2.2.10 on 2020-03-12 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarship', '0018_applied_schlarships'),
    ]

    operations = [
        migrations.AddField(
            model_name='applied_schlarships',
            name='user',
            field=models.ForeignKey(default=32, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
