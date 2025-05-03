from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from .model import Site
from .schema import SiteSchema

router = Router(tags=["Site"])


@router.get("", response=list[SiteSchema])
@paginate
def list_sites(request, workshop_id: int | None = None):
    queryset = Site.objects.all()
    if workshop_id:
        queryset = queryset.filter(workshop_id=workshop_id)
    return queryset


@router.get("{site_id}/", response=SiteSchema)
def get_site(request, site_id: int):
    return get_object_or_404(Site, id=site_id)
