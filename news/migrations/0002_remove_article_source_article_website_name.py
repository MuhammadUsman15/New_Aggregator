# Generated by Django 5.0.3 on 2024-03-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='source',
        ),
        migrations.AddField(
            model_name='article',
            name='website_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
