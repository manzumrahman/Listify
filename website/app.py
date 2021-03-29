import flask
import flask_sqlalchemy
import datetime

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Secret_key'

db = flask_sqlalchemy.SQLAlchemy(app)


class Todo(db.Model):
    serial = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    # holder = db.Column(db.String(200), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f"{self.serial}-{self.title}"


@app.route("/")
def home():
    return flask.render_template('index.html')


@app.route('/app', methods=["GET", "POST"])
def main():
    request = flask.request
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        new_task = Todo(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        flask.flash("New Task Added Successfully!", "success")
    tasks = Todo.query.all()
    return flask.render_template('app.html',task_list=tasks)


@app.route('/delete/<serial>')
def delete(serial):
    task = Todo.query.filter_by(serial=serial).first()
    db.session.delete(task)
    db.session.commit()
    flask.flash("Task Removed Successfully!", "danger")
    return flask.redirect('/app')


@app.route('/update/<serial>', methods=["GET", "POST"])
def update(serial):
    request = flask.request
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        task = Todo.query.filter_by(serial=serial).first()
        task.title = title
        task.description = description
        db.session.add(task)
        db.session.commit()
        flask.flash("Task Updated Successfully!", "success")
        return flask.redirect('/app')
    task = Todo.query.filter_by(serial=serial).first()
    return flask.render_template("update.html", task=task)
