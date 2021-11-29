from datetime import datetime
from flask import Flask, request, render_template, redirect
import connection
import data_manager
import util
from pathlib import Path

UPLOAD_FOLDER = Path('static/images/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route('/list', methods=['GET', 'POST'])
def main_page():
    headers = ['submission time', 'number of views', 'number of votes', 'title', 'message']
    data = connection.read_file('sample_data/question.csv')
    data_manager.convert_time(data)
    if request.method == 'GET':
        category = request.args.get('by_category')
        order = request.args.get('by_order')
        data_manager.sort_data('question', category, order)

    return render_template('list_questions.html', data=data, headers=headers)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question_with_answers(question_id):
    question = data_manager.get_question_by_id_number(question_id)
    question_submission_time = datetime.utcfromtimestamp(float(question['submission_time'])).strftime('%Y-%m-%d - %H:%M:%S')
    question['view_number'] = str(int(question['view_number']) + 1)
    data_manager.update_question(question)
    answers_data_base = data_manager.get_answer_by_question_id(question_id)
    answers_data_base = data_manager.convert_time(answers_data_base)
    image=question['image']
    data_questions = connection.read_file('sample_data/question.csv')
    data_questions = data_manager.convert_time(data_questions)
    data_answers = connection.read_file('sample_data/answer.csv')
    data_answers = data_manager.convert_time(data_answers)

    if request.method == 'GET':
        category = request.args.get('by_category')
        order = request.args.get('by_order')
        data_manager.sort_data('answer', category, order)
    if request.method == 'POST':
        if request.form.get('vote_answer'):
            id = request.form['vote_answer']
            add = int(request.form['vote'])
            data_manager.add_vote(id, add, data_answers)
            connection.save_file(data_answers, 'sample_data/answer.csv')
            data_manager.convert_time(data_answers)
        if request.form.get('vote_question'):
            id = request.form['vote_question']
            add = int(request.form['vote'])
            data_manager.add_vote(id, add, data_questions)
            connection.save_file(data_questions, 'sample_data/question.csv')
            data_manager.convert_time(data_questions)
    return render_template('display_a_question.html',question=question,submission_time=question_submission_time,
                               image=image,answers_base=answers_data_base)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    question = data_manager.get_question_by_id_number(question_id)
    if request.method == 'POST':
        description = request.form['description']
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        answer = util.get_answer(description, file.filename, question_id)
        data_manager.ask_question_answer(answer)     
        return redirect(f'/question/{question_id}')

    elif request.method == 'GET':
        return render_template('upload_answer.html', question_id=question['id'])



@app.route('/add_question', methods=['POST', 'GET'])
def new_question():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        question = util.get_question(title, description, file.filename)
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        data_manager.ask_question(question)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('upload_question.html')


@app.route('/question/<question_id>/delete', methods=['POST', 'GET'])
def delete_question(question_id):
    question = data_manager.get_question_by_id_number(question_id)
    if request.method == 'POST':
        data_manager.delete_question(question)
        return render_template('delete_question.html')
    elif request.method == 'GET':
        return redirect('/')

@app.route('/question/<question_id>/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(question_id, answer_id):
    if request.method == 'POST':
        data_manager.delete_answer(question_id, answer_id)
        return render_template('delete_answer.html')

@app.route('/question/<question_id>/edit_page', methods=['GET', 'POST'])
def edit_question(question_id):
    edited_question = data_manager.get_question_by_id_number(question_id)
    question_submission_time = datetime.utcfromtimestamp(int(float(edited_question['submission_time']))).strftime('%Y-%m-%d %H:%M')
    if request.method == 'POST':
        edited_question['title'] = request.form['title']
        edited_question['message'] = request.form['message']
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        data_manager.update_question(edited_question)
        return redirect(f'/question/{question_id}')

    elif request.method == 'GET':
        return render_template('edit_question.html', question=edited_question, submission_time=question_submission_time)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
