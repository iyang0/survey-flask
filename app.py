from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """base case, start a survey"""
    session["responses"] = []
    
    return render_template("survey_start.html",
        title="Choose your survey",
        instructions="Please fill out the survey")
        
@app.route("/begin", methods=["POST"])
def survey_redirect():
    """redirect after starting the survey"""
    session["survey_key"] = request.form["survey"]
    return redirect("/questions/0")

@app.route("/questions/<int:question_index>")
def questions(question_index):
    """ask question from the survey based on how many answered before"""
    survey = surveys[session["survey_key"]]
    
    if question_index != len(session["responses"]):
        #if user tries to access question out of order, redirect them to correct question.
        flash("You tried to access an invalid question")
        return redirect(f"/questions/{len(session['responses'])}")
        
    elif len(session["responses"]) == len(survey.questions):
        #if user tries to access a question after completing the survey redirect them back to the thanks
        flash("You have already finished the survey")
        return redirect("/thanks")
    else:
        return render_template("question.html",
            question=survey.questions[question_index])

@app.route("/answer",methods=["POST"])
def answer_redirect():
    """appends response with the user's answer and redirects to another question or a thank you page"""
    answer = request.form["answer"]
    comment = request.form.get("comment")
    if comment:
        answer = (answer, comment)
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    survey = surveys[session["survey_key"]]
    
    if len(responses) >= len(survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def completion():
    """render thank you page when survey completed"""
    print(session["responses"])
    return render_template("completion.html")
