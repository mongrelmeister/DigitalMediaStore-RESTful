from app.extensions.database import BaseModelMixin, db


class Album(db.Model, BaseModelMixin):
    __tablename__ = "Album"
    id = db.Column(name="AlbumId", type_=db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(name="Title", type_=db.Unicode(160), nullable=False, unique=True)
    artist_id = db.Column("ArtistId", db.Integer, db.ForeignKey("Artist.ArtistId"), nullable=False)

    def __repr__(self):
        return f"<Albums {self.title}>"

    def __str__(self):
        return self.name

    @classmethod
    def find_album_by_name(cls, title):
        return cls.simple_filter(title=title).first()
