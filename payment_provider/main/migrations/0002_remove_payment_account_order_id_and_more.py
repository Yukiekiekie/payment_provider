# Generated by Django 4.2.1 on 2023-05-12 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment_account",
            name="order_id",
        ),
        migrations.AlterField(
            model_name="payment_account",
            name="balance",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="payment_account",
            name="username",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]