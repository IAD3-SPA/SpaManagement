# Generated by Django 4.1.7 on 2023-04-25 21:30
import os
import shutil

from django.core.files import File
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpaApp', '0009_delete_deficit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('service_status', models.BooleanField(default=True)),
            ],
        ),
    ]
