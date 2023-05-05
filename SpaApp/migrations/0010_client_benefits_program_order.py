# Generated by Django 4.1.7 on 2023-05-04 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SpaApp', '0009_delete_deficit'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='benefits_program',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('refunded', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SpaApp.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SpaApp.product')),
            ],
        ),
    ]
