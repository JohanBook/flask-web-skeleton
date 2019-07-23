from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/get")
def api_route():
    return {"api": True}
