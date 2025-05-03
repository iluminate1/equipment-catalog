from django.shortcuts import render
from django.views import View


class EquipmentCatalogView(View):
    template_name = "equipment/catalog.html"

    def get(self, request):
        return render(request, self.template_name)


class EquipmentDetailView(View):
    template_name = "equipment/detail.html"

    def get(self, request, equipment_id):
        return render(
            request,
            self.template_name,
            {"equipment_id": equipment_id},
        )
