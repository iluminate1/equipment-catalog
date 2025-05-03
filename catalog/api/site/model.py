from django.db import models


class Site(models.Model):
    """Model representing a site within a workshop"""

    name = models.CharField(
        max_length=100,
        verbose_name="Site name",
    )
    workshop = models.ForeignKey(
        "Workshop",
        on_delete=models.CASCADE,
        related_name="sites",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )

    class Meta:
        ordering = (
            "workshop",
            "name",
        )
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return f"{self.workshop.name} - {self.name}"
