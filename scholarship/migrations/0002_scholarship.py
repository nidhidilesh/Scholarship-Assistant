# Generated by Django 2.2.10 on 2020-03-01 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='scholarship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('type', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('income', models.IntegerField()),
                ('qualification', models.CharField(max_length=2000)),
                ('department', models.CharField(max_length=2000)),
                ('aim', models.CharField(max_length=2000)),
                ('link', models.CharField(max_length=2000)),
                ('helpline', models.IntegerField()),
            ],
        ),
    ]
