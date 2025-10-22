import os
import json
from flask import Flask, render_template, request, make_response, url_for, redirect

# Creates flask app
app = Flask(__name__)

ROOT_DIR = os.getcwd()
answers = {}

subject_map = {
    "0455": "IGCSE/Economics-0455",
    "0610": "IGCSE/Biology-0610",
    "0620": "IGCSE/Chemistry-0620",
    "0625": "IGCSE/Physics-0625",
    "0653": "IGCSE/Science-Combined-0653",
    "2281": "O-Level/Economics-2281",
    "5054": "O-Level/Physics-5054",
    "5070": "O-Level/Chemistry-5070",
    "5090": "O-Level/Biology-5090",
    "5129": "O-Level/Science-Combined-5129",
    "9700": "A-Level/Biology-9700",
    "9701": "A-Level/Chemistry-9701",
    "9702": "A-Level/Physics-9702",
    "9706": "A-Level/Accounting-9706",
    "9708": "A-Level/Economics-9708",
}

def get_answers(ms_name):
    """Takes the marking scheme name as a parameter, goes through JSON file to find matching name, and grabs the associated answers list"""
    f = open(os.path.join(ROOT_DIR, 'static', 'answers.json'))
    data = json.load(f)
    print(ms_name)
    if ms_name in data.keys():
        return data[ms_name]
    else:
        return False


def get_paper_name(subj, year, month, variant, ce, alevel):
    """Gets paper name, for statistics and pdf.html title"""
    if ce == '1' and alevel == 'a2-level':
        ce = '3'
    if month == 'm' and year == '22':
        url_month = 'Feb-March'
    elif month == 'm' and year != '22':
        url_month = 'March'
    elif month == 's':
        url_month = 'May-June'
    else:
        url_month = 'Oct-Nov'
    
    return f"{subject_map[subj]}/20{str(year)}-{url_month}/{subj}_{month}{str(year)}_ms_{ce}{variant}.pdf"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/pdf", methods=['GET', 'POST'])
def pdf_display():
    if request.method == 'GET':
        return "The URL / is accessed directly. Try going to '/' to submit the form."

    subj, year, month, variant, ce, alevel = request.form.get('subject', ''), request.form.get('year', ''), request.form.get(
        'month', ''), request.form.get('variant', ''), request.form.get('level', ''), request.form.get('alevel', '')

    if request.method == 'POST':
        paper_name = get_paper_name(subj, year, month, variant, ce, alevel)
        answers = get_answers(paper_name.split('/')[3])
        print(paper_name)
        if (answers == False):
            return redirect(url_for('.index', flag=answers))

        resp = make_response(render_template(
            'pdf.html', answers=answers, paper_name=paper_name))
        return resp

@app.route('/pdf_score', methods=['POST'])
def pdf_score():
    paper_name, correct_answers, user_answers = request.form.get('paper_name', ''), request.form.get(
        'correct_answers', '').split(","), request.form.get('user_answers', '').split(",")
    if request.method == 'POST':
        resp = make_response(render_template('pdf_score.html', paper_name=paper_name,
                             correct_answers=correct_answers, user_answers=user_answers))
        return resp

@app.route('/statistics')
def statistics():
    """Page displaying all user attempted papers and scores in them."""
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)
