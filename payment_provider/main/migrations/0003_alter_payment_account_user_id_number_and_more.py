# Generated by Django 4.2.1 on 2023-05-12 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_remove_payment_account_order_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment_account",
            name="user_id_number",
            field=models.CharField(max_length=18),
        ),
        migrations.AlterField(
            model_name="payment_order",
            name="invoice_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
