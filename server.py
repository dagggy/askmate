from flask import Flask, request, render_template, redirect
import data_manager
import util
from pathlib import Path

UPLOAD_FOLDER = Path('static/images/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route('/list', methods=['GET', 'POST'])
def main_page():
    data = data_manager.get_question_bd()
    for question in data:
        question['submission_time'] = question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    headers = ['submission time', 'number of views', 'number of votes', 'title', 'message']
    if request.method == 'GET':
        category = request.args.get('by_category')
        order = request.args.get('by_order')
        data_manager.sort_data(data, category, order)
    return render_template('list_questions.html', data=data, headers=headers)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question_with_answers(question_id):
    data_manager.get_question_by_id_bd(question_id)
    answers_data_base = data_manager.get_answer_by_question_id_bd(question_id)
    if request.method == 'GET':
        category = request.args.get('by_category')
        order = request.args.get('by_order')
        data_manager.sort_data(answers_data_base, category, order)
    if request.method == 'POST':
        if request.form.get('vote_answer'):
            id = request.form['vote_answer']
            add = int(request.form['vote'])
            data_manager.update_answer_by_vote_bd(id, add)
        if request.form.get('vote_question'):
            id = request.form['vote_question']
            add = int(request.form['vote'])
            data_manager.update_question_by_vote_bd(id, add)
    question = data_manager.get_question_by_id_bd(question_id)[0]
    question['submission_time'] = question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    try:
        image = question['image']
    except:
        image = None
    for answer in answers_data_base:
        answer['submission_time'] = answer['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    comments = data_manager.get_comment_by_question_id_bd(question_id)
    for comment in comments:
        comment['submission_time'] = comment['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    return render_template('display_a_question.html', question=question, image=image, answers_base=answers_data_base, comments=comments)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    question = data_manager.get_question_by_id_bd(question_id)[0]
    if request.method == 'POST':
        description = request.form['description']
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        data_manager.adding_new_answer_bd(question_id, description, file.filename)
        return redirect(f'/question/{question_id}')
    elif request.method == 'GET':
        return render_template('upload_answer.html', question_id=question['id'])


@app.route('/add_question', methods=['POST', 'GET'])
def new_question():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        data_manager.adding_new_question_bd(title, description, file.filename)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('upload_question.html')


@app.route('/question/<question_id>/delete', methods=['POST', 'GET'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_question_by_id_bd(question_id)
        return render_template('delete_question.html')
    elif request.method == 'GET':
        return redirect('/')


@app.route('/question/<question_id>/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(question_id, answer_id):
    if request.method == 'POST':
        data_manager.delete_answer_by_id_bd(question_id, answer_id)
        return render_template('delete_answer.html')


@app.route('/question/<question_id>/edit_page', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_question = request.form['message']
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        data_manager.update_question_by_id_bd(question_id, new_title, new_question, file.filename)
        return redirect(f'/question/{question_id}')
    elif request.method == 'GET':
        edited_question = data_manager.get_question_by_id_bd(question_id)[0]
        edited_question['submission_time'] = edited_question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
        return render_template('edit_question.html', question=edited_question)


@app.route('/question/<question_id>/new_comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    question = data_manager.get_question_by_id_bd(question_id)[0]
    if request.method == 'POST':
        comment_text = request.form['description']
        data_manager.adding_new_comment_to_question_bd(comment_text, question_id)
    return render_template('add_comment_to_question.html', question=question)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
