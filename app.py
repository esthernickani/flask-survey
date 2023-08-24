from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__, template_folder = "templates")
app.config['SECRET_KEY'] = "oh-so-secret"

if __name__ == "__main__":
    app.debug = True
    app.run()

toolbar = DebugToolbarExtension(app)
responses = []



@app.route('/')
def start_survey():
    """Show the title of the survey, instructions and button to start the survey"""
    session['responses'] = []
    title = satisfaction_survey.title
    instruction = satisfaction_survey.instructions
    return render_template("base.html", title=title, instruction=instruction)


@app.route('/questions/<int:idx>')
def show_question(idx):
    """Show the question"""
    responses = session.get('responses', [])
    if len(responses) == 0:
        question = satisfaction_survey.questions[0].question
        choices = satisfaction_survey.questions[0].choices
        index = 0
        return render_template("questions.html", question=question, choices=choices, index=index)
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou.html')
    
    if idx != len(responses):
        flash("This is an invalid question")
        return redirect('/questions/{}'.format(len(responses)))
    
    question = satisfaction_survey.questions[idx].question
    choices = satisfaction_survey.questions[idx].choices
    index = idx
    return render_template("questions.html", question=question, choices=choices, index=index)
        
    


@app.route('/answer', methods=["POST"])
def answer_question():
    """Appends the answer to the responses array and redirects to the next question"""
    responses = session.get('responses', [])
    answer = request.form['answer']
    responses.append(answer)
    session['responses'] = responses

    idx = int(request.form["index"])
    current_idx = idx + 1

    if len(responses) == len(satisfaction_survey.questions):
        return render_template('/thankyou.html')
    else:
        return redirect('/questions/{}'.format(current_idx))


