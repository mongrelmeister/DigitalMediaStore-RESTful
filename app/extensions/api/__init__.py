from flask_smorest import Api as Flask_Smorest_Api
from flask_smorest import Blueprint as Flask_Smorest_Blueprint
from flask_smorest import Page

# Define custom converter to schema function
# def customconverter2paramschema(converter):
#     return {'type': 'custom_type', 'format': 'custom_format'}


class Api(Flask_Smorest_Api):
    """Api override"""

    def __init__(self, app=None, *, spec_kwargs=None):
        spec_kwargs = spec_kwargs or {}
        super().__init__(app, spec_kwargs=spec_kwargs)
        # self.spec.components.security_scheme("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})

        # Register custom Marshmallow fields in doc
        # self.register_field(CustomField, 'type', 'format')

        # Register custom Flask url parameter converters
        # api.register_converter(CustomConverter, customconverter2paramschema)


class Blueprint(Flask_Smorest_Blueprint):
    """Blueprint override"""


class CursorPage(Page):
    """Cursor Pager"""

    # https://flask-smorest.readthedocs.io/en/latest/pagination.html
    @property
    def item_count(self):
        return self.collection.count()
