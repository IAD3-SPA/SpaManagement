from django.db import models


class ProductDelivery(models.Model):
    """Delivery Man fills only those fields"""
    delivery_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()
    # We could add Delivery Man ID or Name

    def __str__(self):
        return f"{self.name}_{self.delivery_id}: {self.date}"

    def save(self, *args, **kwargs):
        try:
            product = Product.objects.get(name=self.name)
        except Product.DoesNotExist:
            raise ValueError(f"{self.name} product does not exist")

        super().save(*args, **kwargs)

        Storage.objects.create(product=product, delivery=self)


class Product(models.Model):
    """We have our own database of products we sell"""
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField()
    price = models.FloatField()
    expiry_duration = models.DurationField()

    def __str__(self):
        return self.name


class Storage(models.Model):
    """Storage Model stores current quantity"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE)
    expiry_date = models.DateField()

    def __str__(self):
        return f"{str(self.product)}: {self.delivery.date}"

    class Meta:
        unique_together = ('product', 'delivery')

    def save(self, *args, **kwargs):
        self.expiry_date = self.delivery.date + self.product.expiry_duration
        super().save(*args, **kwargs)
