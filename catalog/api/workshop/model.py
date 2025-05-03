from django.db import models


class Workshop(models.Model):
    """Model representing a workshop where equipment is located"""

    name = models.CharField(
        max_length=100,
        verbose_name="Workshop name",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    location = models.CharField(
        max_length=200,
        verbose_name="Location",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"

    def __str__(self):
        return str(self.name)
