from flask import Flask, render_template, redirect, url_for, request
from random import shuffle
from my_model import db, Respondents, Answers
from sqlalchemy import insert

# from sqlite3 import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_form.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)

db.create_all()


@app.route("/")
def index():
    return redirect(url_for("main"))


@app.route("/main")
def main():
    lottery = ["badluck"] * 11 + ["/main"]
    shuffle(lottery)
    return render_template("main.html", lottery=lottery)


@app.route("/badluck")
def badluck():
    lottery = ["badluck"] * 11 + ["/main"]
    shuffle(lottery)
    return render_template("bad luck.html", lottery=lottery)


@app.route("/questions")
def questions():
    lottery = ["badluck"] * 11 + ["/main"]
    shuffle(lottery)
    return render_template("questions.html", lottery=lottery)


index = 1


@app.route("/submit")
def submit():
    lottery = ["badluck"] * 11 + ["/main"]
    shuffle(lottery)

    global index

    mothername = request.values.get("mothername")
    age = request.values.get("age")
    height = request.values.get("height")

    respondent = Respondents(
        person_id=index, mothername=mothername, age=age, height=height
    )

    try:
        db.session.add(respondent)
        db.session.commit()
        db.session.refresh(respondent)
    except Exception as exception:
        index += 1
        db.session.add(respondent)
        db.session.commit()
        db.session.refresh(respondent)
        print(exception, 'occured')
    assistant = request.values.get("assistant")
    check = request.values.get("check")
    likes = request.values.get("likes")

    if not assistant:
        assistant = 0
    if not check:
        check = 0
    if not likes:
        likes = 0
    extent = request.values.get("extent")

    design = request.values.get("design")
    content = request.values.get("content")
    author = request.values.get("author")

    if not design:
        design = 0
    if not content:
        content = 0
    if not author:
        author = 0
    author_name = request.values.get("author_name")

    impression = request.values.get("impression")

    answers = Answers(
        person_id=index,
        assistant=assistant,
        check=check,
        likes=likes,
        extent=extent,
        design=design,
        content=content,
        author=author,
        author_name=author_name,
        impression=impression,
    )

    db.session.add(answers)
    db.session.commit()
    db.session.refresh(answers)

    index += 1

    return render_template("submit.html", lottery=lottery)


@app.route("/stats")
def stats():
    lottery = ["badluck"] * 11 + ["/main"]
    shuffle(lottery)
    all_respondents = Answers.query.all()
    total_answers = len(all_respondents)
    assistants = [i for i in all_respondents if i.assistant]
    checking = [i for i in all_respondents if i.check]
    design = [i for i in all_respondents if i.check]
    content = [i for i in all_respondents if i.content]
    author = [i for i in all_respondents if i.author]
    incorrect = [i for i in all_respondents if not i.author_name == "mk"]

    all_respondents = Respondents.query.all()
    try:
        max_age = max([i.age for i in all_respondents if i.age])
    except ValueError:
        max_age = 239
    try:
        max_height = max([i.height for i in all_respondents if i.height])
    except ValueError:
        max_height = 164
    if not isinstance(max_height, int):
        max_height = 164
    if not isinstance(max_age, int):
        max_age = 111
    return render_template(
        "stats.html",
        lottery=lottery,
        total_answers=total_answers,
        assistants=len(assistants),
        checking=len(checking),
        design=len(design),
        content=len(content),
        author=len(author),
        incorrect=len(incorrect),
        max_age=max_age,
        max_height=max_height,
    )


if __name__ == "__main__":
    app.run(debug=False)
