# Generated by Django 4.0.4 on 2022-05-29 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_generatec'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatec',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='generatec',
            name='len',
            field=models.IntegerField(default=1),
        ),
    ]
