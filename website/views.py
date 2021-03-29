from flask import Blueprint,render_template, request, flash, redirect
from flask_login import current_user
from .models import Tasks
from . import db

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template('index.html', user=current_user, thumbnail="../static/thumbnail.png")


@views.route('/app', methods=["GET", "POST"])
def main():
    if current_user.is_authenticated:
        if request.method == "POST":
            title = request.form.get('title')
            description = request.form.get('description')
            new_task = Tasks(title=title, description=description, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("New Task Added Successfully!", "success")
        return render_template('app.html', user=current_user)
    flash("You Need To Login to Access this Page", "danger")
    return redirect('/login')


@views.route('/delete/<serial>')
def delete(serial):
    if current_user.is_authenticated:
        task = Tasks.query.filter_by(serial=serial).first()
        if task and task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
            flash("Task Removed Successfully!", "success")
        else:
            flash('Task Not Found', 'danger')
        return redirect('/app')
    flash("You Need To Login to Access this Page", 'danger')
    return redirect('/login')


@views.route('/update/<serial>', methods=["GET", "POST"])
def update(serial):
    if current_user.is_authenticated:
        task = Tasks.query.filter_by(serial=serial).first()
        if task and task.user_id == current_user.id:
            if request.method == "POST":
                title = request.form.get('title')
                description = request.form.get('description')
                task = Tasks.query.filter_by(serial=serial).first()
                task.title = title
                task.description = description
                db.session.add(task)
                db.session.commit()
                flash("Task Updated Successfully!", "success")
                return redirect('/app')
            return render_template("update.html", task=task, user=current_user)
        else:
            return redirect('/app')
    flash("You Need To Login to Access this Page", 'danger')
    return redirect('/login')

