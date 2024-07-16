from functools import cached_property
from typing import List
from urllib.request import Request

from fastapi import FastAPI
from sqladmin import ModelView, Admin

# from app.admin.admin import CustomAdmin
# from app.admin.auth import AdminAuth
from app.common.security import get_password_hash
from app.db.session import engine
from app.models import user_adventure, adventure, user, mission, objective
from app.models.user import User


class BaseModelView(ModelView):
    page_size = 25
    page_size_options = [10, 25, 50, 100, 200]
    list_template = 'custom_list_view.html'
    sortable_relation_fields = []

    def __init__(self):
        super().__init__()
        self._sort_fields = [
            self._get_prop_name(attr) for attr in
            self.non_relation_fields + self.sortable_relation_fields
        ]

    @cached_property
    def non_relation_fields(self):
        return [prop for prop in self._prop_names if
                prop not in self._mapper.relationships]

    def get_export_columns(self) -> List[str]:
        """Get list of properties to export."""
        return self._build_column_list(
            [],
            include=self.non_relation_fields,
        )


class UserAdventureAdmin(BaseModelView, model=user_adventure.UserAdventure):
    column_list = '__all__'


class AdventureAdmin(BaseModelView, model=adventure.Adventure):
    column_list = '__all__'


class MissionAdmin(BaseModelView, model=mission.Mission):
    column_list = '__all__'


class ObjectiveAdmin(BaseModelView, model=objective.Objective):
    column_list = '__all__'


class UserAdmin(BaseModelView, model=user.User):
    column_list = ['id', 'first_name', 'last_name', 'email', 'is_superuser']
    icon = "fa-solid fa-user"
    column_searchable_list = ['first_name', 'last_name', 'email']

    async def on_model_change(self, data: dict, model: User, is_created: bool, request: Request) -> None:
        """Update model before any db change.

        Args:
            data (dict): Input form.
            model (User): Output User model.
            is_created (bool): Flag if model is now created.
            request (Request): Request.
        """
        if data["hashed_password"] == model.hashed_password:
            return

        if data["hashed_password"] is not None and data["hashed_password"] != "":
            data["hashed_password"] = get_password_hash(data["hashed_password"])


def setup_admin_panel(app: FastAPI):
    # authentication_backend = AdminAuth("")
    admin = Admin(app, engine, templates_dir='admin/templates')
    admin.add_view(AdventureAdmin)
    admin.add_view(MissionAdmin)
    admin.add_view(ObjectiveAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(UserAdventureAdmin)
    return admin
