from django.urls import path

from api.views import EquipmentCatalogView, EquipmentDetailView

app_name = "API View"

urlpatterns = [
    path(
        "",
        EquipmentCatalogView.as_view(),
        name="equipment-catalog",
    ),
    path(
        "equipment/<int:equipment_id>/",
        EquipmentDetailView.as_view(),
        name="equipment-detail",
    ),
]
