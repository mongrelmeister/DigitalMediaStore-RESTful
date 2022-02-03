from flask.views import MethodView

from app.extensions.api import Blueprint

blp = Blueprint("Hello", __name__, url_prefix="/hello", description="Hello World!")


@blp.route("/")
@blp.doc(description="Testing Resource API")
class HelloWorld(MethodView):
    @blp.etag
    def get(self):
        """Hello World!
        ---
        The server is suposed to run run run run
        """
        return {"hello": "world"}
