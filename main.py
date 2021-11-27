
from flask_login import LoginManager
import os
from flask import Flask
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_bcrypt import Bcrypt
from flask_security import (
    Security,
    SQLAlchemySessionUserDatastore,
    SQLAlchemyUserDatastore,
)




app = Flask(__name__, template_folder="templates")
if os.getenv("ENV", "development") == "production":
    raise Exception("Currently no production config is setup.")
else:
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
api = Api(app)
security=Security(app)
login_manager = LoginManager(app)
bcrypt=  Bcrypt(app)
app.app_context().push()
login_manager.login_view='login'


from application.models import User
# Import all the controllers so they are loaded
from application.controllers import *

# Add all restful controllers


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template("403.html"), 403




from application.api import UserAPI
api.add_resource(UserAPI, "/api/user", "/api/user/<int:user_id>")

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=8080)
