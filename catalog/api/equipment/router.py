from django.shortcuts import get_object_or_404
from ninja import Query, Router, UploadedFile
from ninja.filter_schema import FilterSchema
from ninja.pagination import paginate
from ninja.schema import Field

from .model import Equipment, EquipmentDocument, EquipmentType
from .schema import (
    EquipmentDetailSchema,
    EquipmentDocumentSchema,
    EquipmentFilter,
    EquipmentSchema,
    EquipmentTypeDetailSchema,
    EquipmentTypeSchema,
)

router = Router()


@router.get(
    "",
    response=list[EquipmentSchema],
    tags=["Equipment"],
)
@paginate
def list_equipment(
    request,
    filters: Query[EquipmentFilter],
):
    queryset = Equipment.objects.select_related(
        "equipment_type", "workshop", "site"
    ).all()

    return filters.filter(queryset)


@router.get(
    "/{int:equipment_id}/",
    response=EquipmentDetailSchema,
    tags=["Equipment"],
)
def get_equipment(request, equipment_id: int):
    equipment = get_object_or_404(
        Equipment.objects.select_related("equipment_type", "workshop", "site"),
        id=equipment_id,
    )
    equipment.documents = getattr(equipment, "documents", None)
    return equipment


@router.delete(
    "/{int:equipment_id}/",
    tags=["Equipment"],
)
def delete_equipment(request, equipment_id: int):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    equipment.delete()
    return {"success": True}


@router.get(
    "/types/",
    response=list[EquipmentTypeSchema],
    tags=["Equipment Type"],
)
@paginate
def list_equipment_types(request):
    return EquipmentType.objects.all()


@router.get(
    "/types/{int:type_id}/",
    response=EquipmentTypeDetailSchema,
    tags=["Equipment Type"],
)
def get_equipment_type(request, type_id: int):
    equipment_type = get_object_or_404(EquipmentType, id=type_id)
    equipment_type.specifications = equipment_type.specifications.all()
    return equipment_type


# Document endpoints
@router.post(
    "/{int:equipment_id}/documents/",
    response=EquipmentDocumentSchema,
    tags=["Equipment Document"],
)
def create_document(request, equipment_id: int, document: UploadedFile):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    return EquipmentDocument.objects.create(
        equipment=equipment, name=document.name, document=document
    )


@router.delete(
    "/documents/{int:document_id}/",
    tags=["Equipment Document"],
)
def delete_document(request, document_id: int):
    document = get_object_or_404(EquipmentDocument, id=document_id)
    document.delete()
    return {"success": True}
