from django.db import models


class ProductDelivery(models.Model):
    """Delivery Man fills only those fields"""
    delivery_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()
    # We could add Delivery Man ID or Name


class Product(models.Model):
    """We have our own database of products we sell"""
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField()
    price = models.FloatField()
    expiry_time = models.TimeField()


class Storage(models.Model):
    """Storage Model stores current quantity"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'delivery')
