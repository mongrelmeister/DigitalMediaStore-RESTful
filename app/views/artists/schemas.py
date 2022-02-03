from app.extensions.schema import ma
from app.models.artists import Artist
from app.views.albums.schemas import AlbumSchema


class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist

    id = ma.auto_field(dump_only=True)


class ArtistAlbumsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist

    id = ma.auto_field()
    name = ma.auto_field()
    albums = ma.List(ma.Nested("AlbumSchema", exclude=("artist",)))
