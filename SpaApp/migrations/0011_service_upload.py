# Generated by Django 4.1.7 on 2023-04-27 16:44

from django.db import migrations

import os
import shutil

from django.core.files import File
from django.db import migrations, models


def insert_values(apps, schema_editor):
    service = apps.get_model('SpaApp', 'Service')
    # P7D stands for Period 7 Days
    service.objects.create(code='SER000', service_name='Oriental Massage', image=None, price=100., description="""The treatment begins with a relaxing bath
                                                                                                                 in brightening and improving the condition 
                                                                                                                 of the skin Klawska salt containing minerals. 
                                                                                                                 It will allow you to relax both body and mind""")
    service.objects.create(code='SER001', service_name='China Traditional Massage', image=None, price=150.5, description="""It is based on the concept of Jing 
                                                                                                                            Luo /meridians, energy channels/ and the 
                                                                                                                            conduction of internal Chi / Qi / energy. 
                                                                                                                            It is a pillar of Chinese longevity culture, 
                                                                                                                            and its principles of meridians have illuminated 
                                                                                                                            centuries of Chinese doctors' paths.""")
    service.objects.create(code='SERT02', service_name='Hot Baths', image=None, price=50., description="""It nourishes, smooths and firms the skin of the entire body,
                                                                                                            giving it a glow and extraordinary softness. 
                                                                                                            A glass of prosecco is served with the bath.""")
    service.objects.create(code='SER003', service_name='Rituals', image=None, price=100.5, description="""Classical Thai massage is a combination of acupressure 
                                                                                                            techniques and passive yoga. It uses a mat on which 
                                                                                                            the person being massaged assumes various 
                                                                                                            positions derived from yoga.""")
    _add_image(service, 'Oriental Massage', 'media/products/massage_oil.jpg')
    _add_image(service, 'China Traditional Massage', 'media/products/lavender_oil.jpeg')
    _add_image(service, 'Hot Baths', 'media/products/bath_salts.jpg')
    _add_image(service, 'Rituals', 'media/products/clay_mask.jpeg')

def delete_values(apps, schema_editor):
    service = apps.get_model('SpaApp', 'service')
    service.objects.all().delete()


def _add_image(service_model, name, image_path):
    image_real_path = os.path.join('media', 'images', f'{name.replace(" ", "_")}.jpg')
    if os.path.exists(image_real_path):
        return

    service = service_model.objects.get(service_name=name)
    with open(image_path, 'rb') as f:
        service.image.save(f'{name}.jpg', File(f))


class Migration(migrations.Migration):

    dependencies = [
        ('SpaApp', '0010_service'),
    ]

    operations = [
        migrations.RunPython(insert_values, reverse_code=delete_values)
    ]