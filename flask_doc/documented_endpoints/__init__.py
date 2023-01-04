from flask import Blueprint
from flask_restx import Api

from flask_doc.documented_endpoints.authenticate import namespace as authenticate
from flask_doc.documented_endpoints.homepage import namespace as homepage
from flask_doc.documented_endpoints.restaurant import namespace as restaurant
from flask_doc.documented_endpoints.hotel import namespace as hotel
from flask_doc.documented_endpoints.plan import namespace as plan

blueprint = Blueprint('documented_api', __name__)

api_extension = Api(
    blueprint,
    title='Happy Travel',
    version='1.0',
    description='This is API for Travel module'
)

api_extension.add_namespace(authenticate)
api_extension.add_namespace(homepage)
api_extension.add_namespace(restaurant)
api_extension.add_namespace(hotel)
api_extension.add_namespace(plan)
