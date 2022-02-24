from flask.views import MethodView
from flask_smorest import Page

from app.extensions.api import CursorPage  # noqa:F401
from app.extensions.api import Blueprint
from app.models.genre import Genre

from .schemas import GenreSchema

blp = Blueprint("Genres", __name__, url_prefix="/api/genres", description="API endpoints about Genres")


@blp.route("/")
class Genres(MethodView):
    @blp.etag
    @blp.response(200, GenreSchema(many=True))
    @blp.paginate(Page)
    @blp.doc(description="Get information for multiple Genres")
    def get(self):
        """List Genres"""
        ret = Genre.find_all()
        return ret

    @blp.etag
    @blp.arguments(GenreSchema)
    @blp.response(201, GenreSchema)
    @blp.doc(description="Add information for a single Genre")
    def post(self, new_genre):
        """Add a new Genre"""
        item = Genre(**new_genre)
        item.create()
        return item


@blp.route("/<int:id>")
class TrackById(MethodView):
    @blp.etag
    @blp.response(200, GenreSchema)
    @blp.doc(description="Get information for a single Genre")
    def get(self, id):
        """Get genre by ID"""
        ret = Genre.find_by_id(id)
        return ret

    @blp.etag
    @blp.arguments(GenreSchema)
    @blp.response(200, GenreSchema)
    @blp.doc(description="Update information on a Genre")
    def put(self, data, id):
        """Update an existing Genre"""
        item = Genre.find_by_id(id)
        blp.check_etag(item, GenreSchema)
        GenreSchema().update(item, data)
        item.update()
        return item

    @blp.etag
    @blp.response(204)
    @blp.doc(description="Delete information for a single Genre")
    def delete(self, id):
        """Delete an existing Genre"""
        item = Genre.find_by_id(id)
        blp.check_etag(item, GenreSchema)
        item.delete()
