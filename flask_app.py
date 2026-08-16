from flask import Flask, render_template, request
from sqlalchemy import select
from database import engine
from models import users, recommendation_logs, courses
from workflow import run_workflow

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def recommendations():

    with engine.connect() as conn:
        user_rows = conn.execute(
            select(users.c.id, users.c.name)
        ).fetchall()

    result = None

    if request.method == "POST":

        user_id = int(request.form["user_id"])
        user_text = request.form["user_text"]

        result = run_workflow(
            user_text,
            user_id
        )

    return render_template(
        "recommendations.html",
        users=user_rows,
        result=result
    )
@app.route("/users", methods=["GET", "POST"])
def add_user():

    message = None

    if request.method == "POST":
        name = request.form["name"]

        with engine.begin() as conn:
            conn.execute(
                users.insert().values(name=name)
            )

        message = "User added successfully!"

    return render_template(
        "add_user.html",
        message=message
    )
@app.route("/logs")
def logs():

    with engine.connect() as conn:
        query = (
            select(
                recommendation_logs.c.id,
                recommendation_logs.c.user_id,
                users.c.name.label("user_name"),
                recommendation_logs.c.course_id,
                courses.c.course_name,
                recommendation_logs.c.score,
                recommendation_logs.c.created_at
            )
            .select_from(
                recommendation_logs
                .join(users, recommendation_logs.c.user_id == users.c.id)
                .join(courses, recommendation_logs.c.course_id == courses.c.id)
            )
            .order_by(recommendation_logs.c.created_at.desc())
        )

        log_rows = conn.execute(query).fetchall()

    return render_template(
        "logs.html",
        logs=log_rows
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
