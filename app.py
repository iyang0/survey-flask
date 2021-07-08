from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
responses = []

@app.route("/")
def root():
    print(survey.instructions)
    return render_template("survey_start.html",
        title = survey.title,
        instructions=survey.instructions)
        
@app.route("/begin", methods=["POST"])
def survey_redirect():
    return redirect("/questions/0")

@app.route("/questions/<int:question_index>")
def questions(question_index):
    print(responses)
    return render_template("question.html",
        question = survey.questions[question_index])

@app.route("/answer",methods=["POST"])
def answer_redirect():
    answer = request.form.get("answer")
    responses.append(answer)
    return redirect(f"/questions/{len(responses)}")
