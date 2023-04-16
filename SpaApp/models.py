from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy


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
    image = models.ImageField(blank=True, null=True, upload_to='images/')
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


class _Manager(models.Manager):
    """Parent manager class"""
    def create_user(self, username, first_name, last_name, password, email, is_active=False):
        if not email:
            raise ValueError("Email must be given!")

        if not password:
            raise ValueError("Password must be given!")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,  # to email activate
        )
        user.set_password(password)
        user.save(using=self._db)

        return user


class OwnerManager(_Manager):

    def create_user(self, username, first_name, last_name, password, email, is_active=True):
        return super().create_user(username, first_name, last_name, password, email, is_active)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.OWNER)


class ReceptionistManager(_Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.RECEPTIONIST)


class AccountantManager(_Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ACCOUNTANT)


class SupplierManager(_Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SUPPLIER)


class User(AbstractUser):
    """Custom User model"""
    class Types(models.TextChoices):
        OWNER = "OWNER", "owner"
        RECEPTIONIST = "RECEPTIONIST", "receptionist"
        ACCOUNTANT = "ACCOUNTANT", "accountant"
        SUPPLIER = "SUPPLIER", "supplier"  # deliverer?

    type = models.CharField(
        gettext_lazy("Type"),
        max_length=50,
        choices=Types.choices,
        default=Types.OWNER  #
    )


class Owner(User):
    objects = OwnerManager()
    base_type = User.Types.OWNER

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.OWNER
        return super().save(*args, **kwargs)


class Receptionist(User):
    objects = ReceptionistManager()
    base_type = User.Types.RECEPTIONIST

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.RECEPTIONIST
        return super().save(*args, **kwargs)


class Accountant(User):
    objects = AccountantManager()
    base_type = User.Types.ACCOUNTANT

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.ACCOUNTANT
        return super().save(*args, **kwargs)


class Supplier(User):
    objects = SupplierManager()
    base_type = User.Types.SUPPLIER

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.SUPPLIER
        return super().save(*args, **kwargs)
