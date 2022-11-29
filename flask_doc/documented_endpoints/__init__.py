from flask import Blueprint
from flask_restx import Api
from flask_doc.documented_endpoints.product import namespace as product
from flask_doc.documented_endpoints.category import namespace as category
from flask_doc.documented_endpoints.productV2 import namespace as productV2

blueprint = Blueprint('documented_api', __name__)

api_extension = Api(
    blueprint,
    title='SP17 - Product module',
    version='2.0',
    description='This is API for Product module'
)

api_extension.add_namespace(product)
api_extension.add_namespace(productV2)
api_extension.add_namespace(category)