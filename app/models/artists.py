from app.extensions.database import BaseModelMixin, db
from app.models import Album  # noqa:F401


class Artist(db.Model, BaseModelMixin):
    __tablename__ = "Artist"
    id = db.Column(name="ArtistId", type_=db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(name="Name", type_=db.Unicode(120), nullable=False, unique=True)
    albums = db.relationship(
        "Album", backref=db.backref("artist", cascade_backrefs=False), lazy="select", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Artists {self.name}>"

    def __str__(self):
        return self.name

    # def save(self):
    #     BaseModelMixin.save(self)
    #     self.id

    @classmethod
    def find_artist_by_name(cls, name):
        return cls.simple_filter(name=name).first()
