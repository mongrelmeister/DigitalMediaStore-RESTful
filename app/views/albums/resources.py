from flask.views import MethodView
from flask_smorest import Page

from app.extensions.api import CursorPage  # noqa:F401
from app.extensions.api import Blueprint
from app.models import Album

from .schemas import AlbumArgsSchema, AlbumSchema

blp = Blueprint("Albums", __name__, url_prefix="/api/albums", description="API endpoints about albums")


@blp.route("/")
class Albums(MethodView):
    @blp.etag
    @blp.response(200, AlbumSchema(many=True))
    @blp.paginate(Page)
    @blp.doc(description="Get information for multiple albums")
    def get(self):
        """List albums"""
        ret = Album.find_all()
        return ret

    @blp.etag
    @blp.arguments(AlbumArgsSchema)
    @blp.response(201, AlbumSchema)
    @blp.doc(description="Add information for a single album")
    def post(self, new_album):
        """Add a new album"""
        item = Album(**new_album)
        item.create()
        return item


@blp.route("/<int:id>")
class AlbumById(MethodView):
    @blp.etag
    @blp.response(200, AlbumSchema)
    @blp.doc(description="Get information for a single album")
    def get(self, id):
        """Get album by ID"""
        ret = Album.find_by_id(id)
        return ret

    @blp.etag
    @blp.arguments(AlbumArgsSchema)
    @blp.response(200, AlbumSchema)
    @blp.doc(description="Update information for an album")
    def put(self, data, id):
        """Update an existing album"""
        item = Album.find_by_id(id)
        blp.check_etag(item, AlbumArgsSchema)
        AlbumArgsSchema().update(item, data)
        item.update()
        return item

    @blp.etag
    @blp.response(204)
    @blp.doc(description="Delete information for a single album")
    def delete(self, id):
        """Delete an existing album"""
        item = Album.find_by_id(id)
        blp.check_etag(item, AlbumSchema)
        item.delete()
