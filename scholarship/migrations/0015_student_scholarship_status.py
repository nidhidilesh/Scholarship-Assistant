# Generated by Django 2.2.10 on 2020-03-10 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0014_student_scholarship'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_scholarship',
            name='status',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
