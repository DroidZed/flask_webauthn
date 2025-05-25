from flask import render_template
from flask_openapi3 import APIBlueprint, Tag

bp = APIBlueprint("www", __name__, url_prefix="/", doc_ui=False)


@bp.get("/", summary="index page", tags=[Tag(name="www")])
def index():
    return render_template("index.html")
