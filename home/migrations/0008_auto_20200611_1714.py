# Generated by Django 3.0.4 on 2020-06-11 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
