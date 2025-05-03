from api.site.schema import SiteSchema
from api.workshop.schema import WorkshopSchema
from ninja import Field, FilterSchema
from ninja.orm import ModelSchema

from .model import Equipment, EquipmentDocument, EquipmentSpecification, EquipmentType


class EquipmentSpecificationSchema(ModelSchema):
    class Meta:
        model = EquipmentSpecification
        fields = (
            "id",
            "name",
            "specifications_description",
        )


class EquipmentTypeSchema(ModelSchema):
    class Meta:
        model = EquipmentType
        fields = (
            "id",
            "name",
            "description",
        )


class EquipmentTypeDetailSchema(EquipmentTypeSchema):
    specifications: list[EquipmentSpecificationSchema]


class EquipmentDocumentSchema(ModelSchema):
    class Meta:
        model = EquipmentDocument
        fields = (
            "id",
            "name",
            "document",
            "upload_date",
            "description",
        )


class EquipmentSchema(ModelSchema):
    equipment_type: EquipmentTypeSchema
    workshop: WorkshopSchema
    site: SiteSchema

    class Meta:
        model = Equipment
        fields = "__all__"
        fields_optional = ("image",)


class EquipmentDetailSchema(EquipmentSchema):
    documents: EquipmentDocumentSchema | None = None


class EquipmentFilter(FilterSchema):
    workshop_id: int | None = None
    site_id: int | None = None
    equipment_type_id: int | None = Field(None, alias="type_id")
    status: str | None = None
    search: str | None = Field(
        None,
        json_schema_extra={
            "q": [
                "name__icontains",
                "inventory_number__icontains",
                "description__icontains",
            ],
        },
    )
