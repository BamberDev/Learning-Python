from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task, Category
from flask_alembic import Alembic
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Task_Manager"

db.init_app(app)
alembic = Alembic()
alembic.init_app(app)


@app.route("/")
def index():
    tasks = Task.query.order_by(Task.created_at.asc()).all()
    categories = Category.query.all()
    return render_template("index.html", tasks=tasks, categories=categories)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form.get("description", "")
    category_id = request.form.get("category_id", None)
    due_date = request.form.get("due_date", None)
    due_date = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None

    new_task = Task(
        title=title,
        description=description,
        category_id=category_id,
        due_date=due_date,
    )
    db.session.add(new_task)
    db.session.commit()
    flash("Task added successfully!", "success")
    return redirect(url_for("index"))


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return render_template("error.html", message="Task not found.")

    title_key = f"title-{task_id}"
    description_key = f"description-{task_id}"
    due_date_key = f"due_date-{task_id}"
    category_id_key = f"category_id"

    task.title = request.form.get(title_key)
    task.description = request.form.get(description_key)
    due_date = request.form.get(due_date_key)
    if due_date:
        try:
            task.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return render_template("error.html", message="Invalid due date format.")
    else:
        task.due_date = None

    category_id = request.form.get(category_id_key)
    task.category_id = int(category_id) if category_id else None

    db.session.commit()
    flash(f"Task {task_id} updated successfully!", "info")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    flash(f"Task {task_id} deleted successfully!", "error")
    return redirect(url_for("index"))


@app.route("/categories", methods=["POST"])
def add_category():
    name = request.form["name"]
    if not Category.query.filter_by(name=name).first():
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/categories/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if category:
        Task.query.filter_by(category_id=category_id).update({"category_id": None})
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    if query:
        tasks = Task.query.filter(Task.title.ilike(f"%{query}%")).all()
    else:
        tasks = Task.query.order_by(Task.created_at.asc()).all()
    categories = Category.query.all()
    return render_template("index.html", tasks=tasks, categories=categories)


if __name__ == "__main__":
    app.run(debug=True)
