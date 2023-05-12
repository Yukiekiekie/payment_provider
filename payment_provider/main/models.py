import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(extra_fields["password"])
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class Payment_Account(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    balance = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    user_id_number = models.CharField(max_length=18)
    user_phone = models.IntegerField()
    user_email = models.CharField(max_length=50)
    USERNAME_FIELD = 'username'

    objects = MyUserManager()

    def __str__(self):
        return self.username


class Payment_invoice(models.Model):
    pid = models.AutoField(primary_key=True)
    aid = models.IntegerField()
    Price = models.IntegerField()
    Key = models.CharField(max_length=50)
    order_id = models.IntegerField()
    invoice_id = models.IntegerField(50)
    airline = models.CharField(max_length=255)

    def __str__(self):
        return self.pid


class Payment_order(models.Model):
    payment_order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Payment_Account, on_delete=models.CASCADE)
    invoice_time = models.DateTimeField(auto_now_add=True)
    invoice_description = models.CharField(max_length=50)
    Price = models.IntegerField()
    # 0: Income 1: expenses
    status = models.IntegerField()
    type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.payment_order_id
