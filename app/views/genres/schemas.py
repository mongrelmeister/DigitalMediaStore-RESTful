from app.extensions.schema import ma
from app.models.genre import Genre


class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre

    id = ma.auto_field(dump_only=True)

