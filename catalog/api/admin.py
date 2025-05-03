from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Equipment,
    EquipmentDocument,
    EquipmentSpecification,
    EquipmentType,
    Site,
    Workshop,
)


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "description_short")
    search_fields = ("name", "location", "description")
    list_filter = ("name",)
    ordering = ("name",)

    def description_short(self, obj):
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "workshop", "description_short")
    search_fields = ("name", "workshop__name", "description")
    list_filter = ("workshop",)
    ordering = ("workshop__name", "name")

    def description_short(self, obj):
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description_short")
    search_fields = ("name", "description")
    ordering = ("name",)

    def description_short(self, obj):
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )


@admin.register(EquipmentSpecification)
class EquipmentSpecificationAdmin(admin.ModelAdmin):
    list_display = ("name", "equipment_type", "specifications_description_short")
    search_fields = ("name", "equipment_type__name", "specifications_description")
    list_filter = ("equipment_type",)
    ordering = ("equipment_type__name", "name")

    def specifications_description_short(self, obj):
        return (
            obj.specifications_description[:50] + "..."
            if len(obj.specifications_description) > 50
            else obj.specifications_description
        )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_number",
        "name",
        "equipment_type",
        "workshop",
        "site",
        "status",
        "image_preview",
    )
    search_fields = (
        "name",
        "inventory_number",
        "description",
        "workshop__name",
        "site__name",
    )
    list_filter = ("status", "equipment_type", "workshop", "site")
    ordering = ("inventory_number",)
    readonly_fields = ("created_at", "updated_at", "image_preview")
    fieldsets = (
        (
            None,
            {"fields": ("name", "inventory_number", "equipment_type", "description")},
        ),
        ("Location", {"fields": ("workshop", "site")}),
        ("Status", {"fields": ("status", "commissioning_date")}),
        ("Media", {"fields": ("image", "image_preview")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return "-"


@admin.register(EquipmentDocument)
class EquipmentDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "equipment_link", "upload_date", "document_link")
    search_fields = (
        "name",
        "equipment__name",
        "equipment__inventory_number",
        "description",
    )
    list_filter = ("upload_date",)
    ordering = ("-upload_date",)
    readonly_fields = ("upload_date", "document_preview")

    def equipment_link(self, obj):
        return format_html(
            '<a href="/admin/yourapp/equipment/{}/change/">{}</a>',
            obj.equipment.id,
            obj.equipment,
        )

    def document_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Download</a>', obj.document.url
        )

    def document_preview(self, obj):
        if obj.document.url.endswith(".pdf"):
            return format_html(
                '<iframe src="{}" style="width:750px; height:1000px;"></iframe>',
                obj.document.url,
            )
        return "No preview available"
