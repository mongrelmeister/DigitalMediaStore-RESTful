from app.extensions.schema import ma
from app.models.albums import Album


class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album

    id = ma.auto_field(dump_only=True)
    artist = ma.Nested("ArtistSchema", dump_only=True)


class AlbumArgsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album
        include_fk = True

    id = ma.auto_field(dump_only=True)
