from ninja import NinjaAPI

from api.auth.router import router as auth_router
from api.equipment.router import router as equipment_router
from api.site.router import router as site_router
from api.workshop.router import router as workshop_router

api = NinjaAPI(csrf=True)
api.add_router("/auth/", auth_router)
api.add_router("/workshops/", workshop_router)
api.add_router("/sites/", site_router)
api.add_router("/equipments/", equipment_router)
