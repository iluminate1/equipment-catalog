from ninja.orm import ModelSchema

from .model import Workshop


class WorkshopSchema(ModelSchema):
    class Meta:
        model = Workshop
        fields = "__all__"
