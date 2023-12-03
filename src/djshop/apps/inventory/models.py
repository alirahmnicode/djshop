from django.db import models


class StockRecord(models.Model):
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE, related_name="stockrecords")
    sku = models.CharField(max_length=64,unique=True ,blank=True, null=True)
    buy_price = models.PositiveIntegerField(blank=True, null=True)
    sale_price = models.PositiveBigIntegerField()
    num_stock = models.PositiveBigIntegerField(default=0)
    threshold_low_stack = models.PositiveIntegerField(blank=True, null=True)

