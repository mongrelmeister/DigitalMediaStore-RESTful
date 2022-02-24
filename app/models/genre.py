from app.extensions.database import BaseModelMixin, db


class Genre(db.Model, BaseModelMixin):
    __tablename__ = "Genre"
    id = db.Column(name="GenreId", type_=db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(name="Name", type_=db.Unicode(120), nullable=False, unique=True)

    def __repr__(self):
        return f"<Genre {self.name}>"

    def __str__(self):
        return self.name

    @classmethod
    def find_genre_by_name(cls, name):
        return cls.simple_filter(name=name).first()
