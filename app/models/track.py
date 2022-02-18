from app.extensions.database import BaseModelMixin, db


class Track(db.Model, BaseModelMixin):
    __tablename__ = "Track"
    id = db.Column(name="TrackId", type_=db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(name="Name", type_=db.Unicode(200), nullable=False, unique=True)
    media_type_id = db.Column(name="MediaTypeId", type_=db.Integer, nullable=False, default=1)
    composer = db.Column(name="Composer", type_=db.Unicode(220))
    milliseconds = db.Column(name="Milliseconds", type_=db.Integer, nullable=False)
    bytes = db.Column(name="Bytes", type_=db.Integer, default=None, nullable=False)
    unit_price = db.Column(name="UnitPrice", type_=db.Numeric(10, 2), nullable=False, default=1)

    # album
    # `TrackId` INT NOT NULL AUTO_INCREMENT,
    # `Name` NVARCHAR(200) NOT NULL,
    # `AlbumId` INT,
    # `Composer` NVARCHAR(220),
    # `Milliseconds` INT NOT NULL,
    #     # `Bytes` INT,
    # `UnitPrice` NUME """RIC(10,2) NOT NULL,

    def __repr__(self):
        return f"<Track {self.name}>"

    def __str__(self):
        return self.name

    # def save(self):
    #    BaseModelMixin.save(self)
    #    self.id

    @classmethod
    def find_track_by_name(cls, name):
        return cls.simple_filter(name=name).first()
