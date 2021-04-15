import flask
import flask_sqlalchemy
from flask_login import LoginManager

db = flask_sqlalchemy.SQLAlchemy()
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ldxqopantlkjxr:b14179a90551c18e5855b5b62d72a2f8e473d40cdad72598eddaa3d717d6bb7c@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d63mk0o6k3ulv6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Secret_key'
db.__init__(app)


def create_app():
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Tasks

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
