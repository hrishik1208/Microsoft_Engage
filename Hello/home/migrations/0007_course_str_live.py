# Generated by Django 4.0.4 on 2022-05-14 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_str',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('course_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Live',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('course_name', models.CharField(max_length=100)),
                ('time_future', models.IntegerField()),
            ],
        ),
    ]
