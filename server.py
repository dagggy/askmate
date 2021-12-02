from flask import Flask, request, render_template, redirect
import data_manager
import util
from pathlib import Path
from markupsafe import Markup

UPLOAD_FOLDER = Path(str(Path(__file__).parent.absolute()) + '/static/images')
QUESTION_TABLE_HEADERS = ['Submission time', 'Number of views', 'Number of votes', 'Title', 'Message']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home_page():
    data = data_manager.get_top_records('question', 'submission_time', size_limit=5)
    for question in data:
        question['submission_time'] = question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    return render_template('home_page.html', data=data, headers=QUESTION_TABLE_HEADERS)

@app.route('/list', methods=['GET', 'POST'])
def list_question_page():
    data = data_manager.get_sorted_data('question')
    for question in data:
        question['submission_time'] = question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    if request.method == 'GET':
        category = request.args.get('by_category')
        order = request.args.get('by_order')
        data = data_manager.get_sorted_data('question', category, order)
    return render_template('list_questions.html', data=data, headers=QUESTION_TABLE_HEADERS)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question_with_answers(question_id):
    comments_to_answer = []
    answers_data_base = data_manager.get_sorted_data('answer', question_id=question_id)
    question = data_manager.get_record_by_primary_key({'id': question_id}, 'question')
    question['submission_time'] = question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    try:
        image = question['image']
    except:
        image = None
    for answer in answers_data_base:
        answer['submission_time'] = answer['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    comments_to_question = data_manager.get_records_by_foreign_key({'question_id': question_id}, 'comment')
    for comment in comments_to_question:
        comment['submission_time'] = comment['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
    number_of_comments_to_question = len(comments_to_question)
    for answer in answers_data_base:
        comment_to_answer = data_manager.get_records_by_foreign_key({'answer_id': answer['id']}, 'comment')
        if comment_to_answer != []:
            comments_to_answer.append(comment_to_answer)
    number_of_comments_to_answer = len(comments_to_answer)
    list_of_tags = []
    list_of_tag_id = data_manager.get_records_by_foreign_key({'question_id': question_id}, 'question_tag',  statement='tag_id')
    for tag_id in list_of_tag_id:
        # list_of_tags.append([data_manager.get_tag_by_tag_id_bd(tag_id['tag_id']), tag_id['tag_id']])
        list_of_tags.append(data_manager.get_records_by_foreign_key({'id': tag_id['tag_id']}, 'tag', statement='name'))

    if request.method == 'POST':
        if request.form.get('vote_answer'):
            id = request.form['vote_answer']
            add = int(request.form['vote'])
            data_manager.update_record(id, {'vote_number': add}, 'answer')
        if request.form.get('vote_question'):
            id = request.form['vote_question']
            add = int(request.form['vote'])
            data_manager.update_record(id, {'vote_number': add}, 'question')
            return redirect(f'/question/{question_id}')
        answers_data_base = data_manager.get_sorted_data('answer', question_id=question_id)

    if request.method == 'GET':
        category = request.args.get('by_category')
        order = request.args.get('by_order')
        answers_data_base = data_manager.get_sorted_data('answer', category, order, question_id)
    return render_template('display_a_question.html', question=question, image=image, number_of_comments_to_answer=number_of_comments_to_answer, answers_base=answers_data_base, comments_to_answer=comments_to_answer, comments_to_question=comments_to_question, number_of_comments_to_question=number_of_comments_to_question, list_of_tags=list_of_tags)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    question = data_manager.get_record_by_primary_key({'id': question_id}, 'question')
    if request.method == 'POST':
        description = request.form['description']
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        data_manager.add_new_answer_record(question_id, description, file.filename)
        return redirect(f'/question/{question_id}')
    elif request.method == 'GET':
        return render_template('upload_answer.html', question_id=question['id'])


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer_data = data_manager.get_record_by_primary_key({'id': answer_id}, 'answer')
    if request.method == 'POST':
        new_message = request.form['description']
        file = request.files['file']
        if file:
            if util.allowed_file(file.filename):
                file.save(UPLOAD_FOLDER / file.filename)
                file = file.filename
            else:
                file = answer_data['image']
        else:
            file = answer_data['image']
        data_manager.update_record(answer_id, {'message': new_message, 'image': file}, 'answer')
        return redirect(f'/question/{answer_data["question_id"]}')
    if request.method == 'GET':
        edited_answer = data_manager.get_record_by_primary_key({'id': answer_id}, 'answer')
        edited_answer['submission_time'] = edited_answer['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
        return render_template('edit_answer.html', answer=edited_answer)


@app.route('/add_question', methods=['POST', 'GET'])
def new_question():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            file.save(UPLOAD_FOLDER / file.filename)
        data_manager.add_new_question_record(title, description, file.filename)
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
        value = list(request.form)
        if value == ['yes']:
            data_manager.delete_answer_by_id_bd(question_id, answer_id)
            return redirect(f'/question/{question_id}')
        else:
            return redirect(f'/question/{question_id}')
    elif request.method == 'GET':
        return render_template('confirm_answer_deletion.html')


@app.route('/question/<question_id>/edit_page', methods=['GET', 'POST'])
def edit_question(question_id):
    question_data = data_manager.get_record_by_primary_key({'id': question_id}, 'question')
    if request.method == 'POST':
        new_title = request.form['title']
        new_question = request.form['message']
        file = request.files['file']
        if file:
            if util.allowed_file(file.filename):
                file.save(UPLOAD_FOLDER / file.filename)
                file = file.filename
            else:
                file = question_data['image']
        else:
            file = question_data['image']
        data_manager.update_record(question_id, {'title': new_title, 'message': new_question, 'image': file }, 'question')
        return redirect(f'/question/{question_id}')

    elif request.method == 'GET':
        edited_question = data_manager.get_record_by_primary_key({'id': question_id}, 'question')
        edited_question['submission_time'] = edited_question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
        return render_template('edit_question.html', question=edited_question)


@app.route('/question/<question_id>/new_comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    question = data_manager.get_record_by_primary_key({'id': question_id}, 'question')
    if request.method == 'POST':
        comment_text = request.form['description']
        data_manager.add_new_comment_to_question_record(comment_text, question_id)
        return redirect(f'/question/{question_id}')
    return render_template('add_comment_to_question.html', question=question)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    answer = data_manager.get_record_by_primary_key({'id': answer_id}, 'answer')
    if request.method == 'POST':
        comment_text = request.form['description']
        data_manager.add_new_comment_to_answer_record(comment_text, answer_id)
        question_id = answer['question_id']
        return redirect(f'/question/{question_id}')
    return render_template('add_comment_to_answer.html', answer=answer)

@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.get_comment_by_id_bd(comment_id);
    answer = data_manager.get_record_by_primary_key(comment["answer_id"], 'answer')
    question = data_manager.get_record_by_primary_key(comment["question_id"], 'question')

    if request.method == 'POST':
        comment_text = request.form['description']
        data_manager.edit_comment_by_id_bd(comment_id, comment_text)
        return redirect(f'/question/{question["id"]}')

    return render_template('edit_comment.html', comment=comment, answer=answer, question=question)


@app.route('/search')
def search_result():
    search_phrase = request.args['search'].lower().strip()
    data = data_manager.search_by_phrase(search_phrase)
    for question in data:
        question['submission_time'] = question['submission_time'].strftime("%d/%m/%Y %H:%M:%S")
        question['message'] = Markup(question['message'].lower().replace(search_phrase, f"<mark>{search_phrase}</mark>"))
        question['title'] = Markup(question['title'].lower().replace(search_phrase, f"<mark>{search_phrase}</mark>"))
    return render_template('list_questions.html', data=data, headers=QUESTION_TABLE_HEADERS)


@app.route('/question/<question_id>/new_tag', methods=['GET', 'POST'])
def add_tag_to_question(question_id):
    question = data_manager.get_record_by_primary_key({'id': question_id}, 'question')
    tags = data_manager.get_all_records('tag')
    if request.method == 'POST':
        if request.form.get('thisistag'):
            tag = request.form.get('thisistag')
            data_manager.add_new_tag(tag)
        elif request.form.get('all_tags'):
            tag = request.form.get('all_tags')
        tag_id = data_manager.get_record_by_primary_key({'name': tag}, 'tag', 'id')
        data_manager.add_tag_to_question_tag_bd(question_id, tag_id['id'])

        return redirect(f'/question/{question["id"]}')
    return render_template('add_tag_to_question.html', question=question, tags=tags)


@app.route('/question/<question_id>/tag/<tag_id>/delete_tag', methods=['GET', 'POST'])
def remove_tag_from_question(question_id, tag_id):
    if request.method == 'POST':
        value = list(request.form)
        if value == ['yes']:
            data_manager.delete_tag_from_question(question_id, tag_id)
            return redirect(f'/question/{question_id}')
        else:
            return redirect(f'/question/{question_id}')
    elif request.method == 'GET':
        return render_template('confirm_tag_deletion.html')
    else:
        return redirect('/')



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
