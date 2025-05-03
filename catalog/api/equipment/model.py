from django.core.validators import FileExtensionValidator
from django.db import models


class EquipmentType(models.Model):
    """Model representing different types of equipment"""

    name = models.CharField(max_length=100, verbose_name="Type name")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        ordering = ("name",)
        verbose_name = "Equipment Type"
        verbose_name_plural = "Equipment Types"

    def __str__(self):
        return str(self.name)


class EquipmentSpecification(models.Model):
    """Model representing possible specifications for equipment types"""

    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name="specifications",
    )
    name = models.CharField(max_length=100, verbose_name="Specification name")
    specifications_description = models.TextField(
        blank=True,
        verbose_name="Specification description",
    )

    class Meta:
        ordering = ("equipment_type", "name")
        verbose_name = "Equipment Specification"
        verbose_name_plural = "Equipment Specifications"
        unique_together = ("equipment_type", "name")

    def __str__(self):
        return f"{self.equipment_type.name} - {self.name}"


class Equipment(models.Model):
    """Model representing a piece of equipment"""

    name = models.CharField(max_length=200, verbose_name="Equipment name")
    inventory_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Inventory number",
    )
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="equipment",
        verbose_name="Equipment type",
    )
    workshop = models.ForeignKey(
        "Workshop",
        on_delete=models.PROTECT,
        related_name="equipment",
        verbose_name="Workshop",
    )
    site = models.ForeignKey(
        "Site",
        on_delete=models.PROTECT,
        related_name="equipment",
        verbose_name="Site",
    )
    image = models.ImageField(
        upload_to="equipment_images/",
        null=True,
        blank=True,
        verbose_name="Equipment image",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    commissioning_date = models.DateField(
        null=True, blank=True, verbose_name="Commissioning date"
    )
    status_choices = (
        ("operational", "Operational"),
        ("maintenance", "Under Maintenance"),
        ("out_of_order", "Out of Order"),
        ("decommissioned", "Decommissioned"),
    )
    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default="operational",
        verbose_name="Status",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )

    class Meta:
        ordering = ("inventory_number",)
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self):
        return f"{self.inventory_number} - {self.name}"


class EquipmentDocument(models.Model):
    """Model representing scanned documents/passports for equipment"""

    equipment = models.OneToOneField(
        Equipment,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Equipment",
    )
    name = models.CharField(max_length=200, verbose_name="Document name")
    document = models.FileField(
        upload_to="equipment_documents/",
        validators=[FileExtensionValidator(("pdf",))],
        verbose_name="Document file",
    )
    upload_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Upload date",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )

    class Meta:
        ordering = ("-upload_date",)
        verbose_name = "Equipment Document"
        verbose_name_plural = "Equipment Documents"

    def __str__(self):
        return f"{self.equipment.inventory_number} - {self.name}"
