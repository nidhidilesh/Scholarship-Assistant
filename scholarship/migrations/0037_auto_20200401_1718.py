# Generated by Django 2.2.10 on 2020-04-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0036_delete_student_scholarship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applied_scholarships',
            name='enrolment',
            field=models.BigIntegerField(),
        ),
    ]
