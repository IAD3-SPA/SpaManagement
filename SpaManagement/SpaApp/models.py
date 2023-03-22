from django.db import models

# Create your models here.

class SimpleTest(models.Model):
    
    randomText = models.CharField(max_length=200)
    randomDate = models.DateTimeField('date published')