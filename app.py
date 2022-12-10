# main.py
from flask import Flask
from flask_doc.documented_endpoints import blueprint as documented_endpoints
from logging import debug
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['RESTPLUS_MASK_SWAGGER'] = False

app.register_blueprint(documented_endpoints)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
