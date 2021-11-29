'''
Utility "layer" | util.py | Helper functions that can be called from any other layer,
but mainly from the business logic layer.
'''
import connection
import time

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'bmp', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_question(title:str, description:str, file:str):
    data = connection.read_file('sample_data/question.csv')
    i=1
    for dict in data:
        if dict['id'] == str(i):
            i += 1
            continue
        else:
            return get_question_data(i, title, description, file)
    return get_question_data(i, title, description, file)


def get_question_data(id, title:str, description:str, file:str):
    return {'id': str(id), 'submission_time':str(int(time.time())), 'view_number':'0', 'vote_number':'0', 'title': title, 'description': description, 'image':file}


def get_answer(message, file, question_id):
    data = connection.read_file('sample_data/answer.csv')
    next_id = int(data[-1]['id']) + 1
    return get_answer_data(next_id, message, file, question_id)


def get_answer_data(id, message, file, question_id):
    return {'id': str(id), 'submission_time':str(int(time.time())), 'vote_number':'0', 'question_id': question_id, 'message':message, 'image':file}