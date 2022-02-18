from app.extensions.schema import ma
from app.models.track import Track


class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Track

    id = ma.auto_field(dump_only=True)

