# import marshmallow
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema

from flask_marshmallow import Marshmallow as FlaskMarshmallowMarshmallow
from flask_marshmallow.sqla import (
    SQLAlchemyAutoSchema as FlaskMarshmallowSQLAlchemyAutoSchema,
)
from flask_marshmallow.sqla import SQLAlchemySchema as FlaskMarshmallowSQLAlchemySchema


class Schema(FlaskMarshmallowSQLAlchemySchema):
    """Schema override"""

    class Meta:
        include_fk = True


class AutoSchema(FlaskMarshmallowSQLAlchemyAutoSchema):
    """SQLAlchemyAutoSchema override"""

    class Meta:
        include_fk = True

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [k for k, v in self.fields.items() if not v.dump_only]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


#     # FIXME: This does not respect allow_none fields
#     @ma.post_dump
#     def remove_none_values(self, data, **kwargs):
#         return {key: value for key, value in data.items() if value is not None}


class Marshmallow(FlaskMarshmallowMarshmallow):
    """Marshmallow override"""

    def __init__(self, app=None):
        super().__init__(app)
        self.SQLAlchemySchema = Schema
        self.SQLAlchemyAutoSchema = AutoSchema


ma = Marshmallow()

# ma = FlaskMarshmallowMarshmallow()
