import hashlib

from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(
        width_field="width", height_field="height", upload_to="images"
    )
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    file_hash = models.CharField(max_length=40, db_index=True)
    file_size = models.PositiveIntegerField(null=True)

    focal_point_x = models.PositiveBigIntegerField(null=True, blank=True)
    focal_point_y = models.PositiveBigIntegerField(null=True, blank=True)
    focal_point_width = models.PositiveBigIntegerField(null=True, blank=True)
    focal_point_height = models.PositiveBigIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        self.file_size = self.image.size

        self.file_hash = self.get_file_hash()
        super().save(*args, **kwargs)

    def get_file_hash(self):
        hasher = hashlib.sha1()

        for chunk in self.image.file.chunk():
            hasher.update(chunk)

        return hasher.digest()
