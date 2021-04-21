import flask
import flask_sqlalchemy
from flask_login import LoginManager

app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Secret_key'
db = flask_sqlalchemy.SQLAlchemy(app)


def create_app(database_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Tasks
    db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
