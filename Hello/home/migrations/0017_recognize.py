# Generated by Django 4.0.4 on 2022-05-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_alter_student_attendace_report_time_present'),
    ]

    operations = [
        migrations.CreateModel(
            name='recognize',
            fields=[
                ('username', models.CharField(max_length=100)),
                ('If_posted', models.IntegerField(primary_key=True, serialize=False)),
                ('Response_charge', models.IntegerField()),
            ],
        ),
    ]
