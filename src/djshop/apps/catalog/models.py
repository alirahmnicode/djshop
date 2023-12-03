from django.db import models
from treebeard.mp_tree import MP_Node
from djshop.apps.catalog.managers import CategoryQueryset
from djshop.libs.db.models import AuditableModel


class Category(MP_Node):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.title

    objects = CategoryQueryset.as_manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class OptionGroup(models.Model):
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"


class OptionGroupValue(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Option Group Value"
        verbose_name_plural = "Option Groups Values"


class ProductClass(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    options = models.ManyToManyField("Option", blank=True)
    track_stock = models.BooleanField(default=True)
    require_shipping = models.BooleanField(default=True)

    @property
    def has_attribute(self):
        return self.attributes.exists()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Class"


class ProductAttribute(models.Model):
    class AttributeTypeChioce(models.TextChoices):
        text = "text"
        intger = "intger"
        float = "float"
        option = "option"
        multi_option = "multi_option"

    product_class = models.ForeignKey(
        ProductClass,
        on_delete=models.CASCADE,
        null=True,
        related_name="attributes",
    )
    title = models.CharField(max_length=64)
    type = models.CharField(
        max_length=16,
        choices=AttributeTypeChioce.choices,
        default=AttributeTypeChioce.text,
    )
    option_group = models.ForeignKey(
        OptionGroup,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    required = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class Option(models.Model):
    class OptionTypeChioce(models.TextChoices):
        text = "text"
        intger = "intger"
        float = "float"
        option = "option"
        multi_option = "multi_option"

    title = models.CharField(max_length=64)
    type = models.CharField(
        max_length=16,
        choices=OptionTypeChioce.choices,
        default=OptionTypeChioce.text,
    )
    option_group = models.ForeignKey(
        OptionGroup,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    required = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"


class Product(AuditableModel):
    class ProductTypeChiose(models.TextChoices):
        standalone = "standalone"
        parent = "parent"
        child = "child"

    structure = models.CharField(
        max_length=16,
        choices=ProductTypeChiose.choices,
        default=ProductTypeChiose.standalone,
    )
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    upc = models.CharField(
        max_length=24, unique=True, null=True, blank=True, db_index=True
    )
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, allow_unicode=True, db_index=True)
    meta_title = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    meta_description = models.TextField(null=True, blank=True)
    produc_class = models.ForeignKey(
        ProductClass,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products",
    )
    attributes = models.ManyToManyField(
        ProductAttribute, through="ProductAttributeValue"
    )
    category = models.ManyToManyField(Category, related_name="categories")

    @property
    def main_image(self):
        if self.images.existe():
            return self.images.first()
        else:
            return None
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    value_text = models.TextField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_option = models.ForeignKey(OptionGroupValue, on_delete=models.PROTECT, null=True, blank=True)
    value_multi_option = models.ManyToManyField(OptionGroupValue, blank=True,
                                                related_name='multi_valued_attribute_value')

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        unique_together = ('product', 'attribute')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ForeignKey("media.Image", on_delete=models.PROTECT)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order",)
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        for i, image in enumerate(self.product.images.all()):
            image.display_order = i
            image.save()
