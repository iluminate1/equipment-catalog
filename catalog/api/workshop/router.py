from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from .model import Workshop
from .schema import WorkshopSchema

router = Router(tags=["Workshop"])


@router.get("", response=list[WorkshopSchema])
@paginate
def list_workshops(request):
    return Workshop.objects.all()


@router.get("{workshop_id}/", response=WorkshopSchema)
def get_workshop(request, workshop_id: int):
    return get_object_or_404(Workshop, id=workshop_id)
