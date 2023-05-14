# Generated by Django 4.1.7 on 2023-05-14 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SpaApp', '0012_merge_20230513_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cosmethologist',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('SpaApp.user',),
        ),
        migrations.AddField(
            model_name='appointment',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='role',
            field=models.CharField(choices=[('OWNER', 'Owner'), ('RECEPTIONIST', 'Receptionist'), ('ACCOUNTANT', 'Accountant'), ('SUPPLIER', 'Supplier'), ('COSMETHOLOGIST', 'Cosmethologist')], default='OWNER', max_length=50, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SpaApp.client'),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('OWNER', 'owner'), ('RECEPTIONIST', 'receptionist'), ('ACCOUNTANT', 'accountant'), ('SUPPLIER', 'supplier'), ('COSMETHOLOGIST', 'cosmethologist')], default='OWNER', max_length=50, verbose_name='Type'),
        ),
    ]
