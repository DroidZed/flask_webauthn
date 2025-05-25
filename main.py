from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from werkzeug.utils import import_string
import orjson
from flask.json.provider import JSONProvider

from src.config.env import Env

api_blueprints = ["passkey_bp", "main_bp"]


class OrJSONProvider(JSONProvider):
    option = orjson.OPT_INDENT_2

    def dumps(self, obj, **kwargs):
        return orjson.dumps(obj, option=self.option).decode()

    def loads(self, s, **kwargs):
        return orjson.loads(s)


def main():
    info = Info(title="Passkey API", version="0.0.0")
    app = OpenAPI(__name__, info=info, template_folder="templates")

    orjson_provider = OrJSONProvider(app)
    app.json = orjson_provider

    bps = api_blueprints
    # Register blueprints
    for bp_name in bps:
        print("Registering bp: %s" % bp_name)
        bp = import_string("src.routes.%s:bp" % bp_name)
        app.register_api(bp)

    return app


if __name__ == "__main__":
    main().run(port=Env().PORT, host=Env().HOST, debug=True)
