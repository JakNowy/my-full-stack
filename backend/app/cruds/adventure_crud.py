from fastcrud import FastCRUD

from app.models.adventure import Adventure


class AdventureCrud(FastCRUD):
    pass


adventure_crud = AdventureCrud(
    Adventure,
)
