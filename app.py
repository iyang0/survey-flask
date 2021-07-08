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
    """base case, start a survey"""
    print(survey.instructions)
    return render_template("survey_start.html",
        title = survey.title,
        instructions=survey.instructions)
        
@app.route("/begin", methods=["POST"])
def survey_redirect():
    """redirect after starting the survey"""
    return redirect("/questions/0")

@app.route("/questions/<int:question_index>")
def questions(question_index):
    """ask question from the survey based on how many answered before"""
    print(responses)
    return render_template("question.html",
        question = survey.questions[question_index])

@app.route("/answer",methods=["POST"])
def answer_redirect():
    """appends response with the user's answer and redirects to another question or a thank you page"""
    answer = request.form.get("answer")
    responses.append(answer)
    if len(responses) >= len(survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def completion():
    """render thank you page when survey completed"""
    return render_template("completion.html")
