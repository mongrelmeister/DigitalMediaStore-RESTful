from flask.views import MethodView
from flask_smorest import Page

from app.extensions.api import CursorPage  # noqa:F401
from app.extensions.api import Blueprint
from app.models import Artist

from .schemas import ArtistAlbumsSchema, ArtistSchema

blp = Blueprint("Artists", __name__, url_prefix="/api/artists", description="API endpoints about artists")


@blp.route("/")
class Artists(MethodView):
    @blp.etag
    # @blp.arguments(ArtistQueryArgsSchema, location="query")
    @blp.response(200, ArtistSchema(many=True))
    @blp.paginate(Page)
    @blp.doc(description="Get information for multiple artists")
    def get(self):
        """List artists"""
        ret = Artist.find_all()
        return ret

    @blp.etag
    @blp.arguments(ArtistSchema)
    @blp.response(201, ArtistSchema)
    @blp.doc(description="Add information for a single artist")
    def post(self, new_artist):
        """Add a new artist"""
        item = Artist(**new_artist)
        item.create()
        return item


@blp.route("/<int:id>")
class ArtistById(MethodView):
    @blp.etag
    @blp.response(200, ArtistSchema)
    @blp.doc(description="Get information for a single artist")
    def get(self, id):
        """Get artist by ID"""
        ret = Artist.find_by_id(id)
        return ret

    @blp.etag
    @blp.arguments(ArtistSchema)
    @blp.response(200, ArtistSchema)
    @blp.doc(description="Update information for an artist")
    def put(self, data, id):
        """Update an existing artist"""
        item = Artist.find_by_id(id)
        blp.check_etag(item, ArtistSchema)
        ArtistSchema().update(item, data)
        item.update()
        return item

    @blp.etag
    @blp.response(204)
    @blp.doc(description="Delete information for a single artist")
    def delete(self, id):
        """Delete an existing artist"""
        item = Artist.find_by_id(id)
        blp.check_etag(item, ArtistSchema)
        item.delete()


@blp.route("/<int:id>/albums")
class ArtistWithAlbums(MethodView):
    @blp.etag
    @blp.response(200, ArtistAlbumsSchema)
    @blp.doc(description="Get information about an artist's albums")
    def get(self, id):
        ret = Artist.find_by_id(id)

        return ret
