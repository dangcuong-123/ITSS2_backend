from flask import Blueprint
from flask_restx import Api

from flask_doc.documented_endpoints.authen import namespace as authen
from flask_doc.documented_endpoints.homepage import namespace as homepage
from flask_doc.documented_endpoints.restaurant import namespace as restaurants

blueprint = Blueprint('documented_api', __name__)

api_extension = Api(
    blueprint,
    title='Happy Travel',
    version='1.0',
    description='This is API for Product module'
)

api_extension.add_namespace(authen)
api_extension.add_namespace(homepage)
api_extension.add_namespace(restaurants)
