from api.workshop.schema import WorkshopSchema
from ninja.orm import ModelSchema

from .model import Site


class SiteSchema(ModelSchema):
    workshop: WorkshopSchema

    class Meta:
        model = Site
        fields = (
            "id",
            "name",
            "description",
        )
