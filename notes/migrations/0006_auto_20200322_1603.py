# Generated by Django 3.0.4 on 2020-03-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_article_context'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='context',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
