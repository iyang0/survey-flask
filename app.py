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
        
@app.route("/begin")
def survey_redirect():
    return redirect("/questions/0")

@app.route("/questions/<question_index>")
def questions(question_index):
    #TODO add questions
    return render_template("question.html")