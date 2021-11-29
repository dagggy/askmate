'''
This is the layer between the server and the data.
Functions here are called from server.py
and use generic functions from connection.py.
'''
from datetime import datetime
import time
import database_common
'''
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
'''

### ????? ###
def add_vote(id, add, answers_data_base):
    for dict in answers_data_base:
        if dict['id'] == id:
            dict['vote_number'] = str(int(dict['vote_number']) + add)
        dict['submission_time'] = str(time.mktime(datetime.strptime(dict['submission_time'], "%Y-%m-%d %H:%M").timetuple()))
    return answers_data_base


@database_common.connection_handler
def get_question_by_id_number(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time, view_number, vote_number, title, message, image 
                    FROM question
                    WHERE id = %(id)s ORDER BY title;
                   """,
                   {'id': question_id})
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time, vote_number, message, title, message, image
                    FROM answer
                    WHERE question_id = %(id)s ORDER BY vote_number;
                   """,
                   {'id': question_id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def ask_question_answer(cursor, new_answer_data):
    new_answer_id = max_id('answer') + 1
    cursor.execute("""
                    INSERT INTO answer
                    VALUES(%(id)s, %(sub_time)s, %(vote)s, %(q_id)s, %(message)s, %(image)s);
                    """,
                    {'id': new_answer_id, 
                    'sub_time': new_answer_data['submission_time'], 
                    'vote': new_answer_data['vote_number'], 
                    'q_id': new_answer_data['question_id'], 
                    'message': new_answer_data['message'], 
                    'image': new_answer_data['image']})


@database_common.connection_handler
def max_id(cursor, database_name):
    cursor.execute("""SELECT MAX(id) FROM %(db)s;""",
                    {'db': database_name})
    max_id = cursor.fetchall()
    return max_id


@database_common.connection_handler
def ask_question(cursor, new_question_data):
    new_question_id = max_id('question') + 1
    cursor.execute("""
                    INSERT INTO question
                    VALUES(%(id)s, %(sub_time)s, %(view)s, %(vote)s, %(title)s, %(message)s, %(image)s);
                    """,
                    {'id': new_question_id, 
                    'sub_time': new_question_data['submission_time'], 
                    'view': new_question_data['view_number'], 
                    'vote': new_question_data['vote_number'], 
                    'title': new_question_data['title'], 
                    'message': new_question_data['message'], 
                    'image': new_question_data['image']})


@database_common.connection_handler
def sort_data(cursor, database_name, order_by, order_direction):
    if order_direction == "Ascending" or None:
        order = 'ASC'
    elif order_direction == "Descending":
        order = 'DESC'
    
    if order_by == "Number of Votes" or None:
        category = "vote_number"
    elif order_by == "Chronology" or 'Submission time':
        category = 'submission_time'
    elif order_by == "Answer length":
        category = "message"
    elif order_by == 'Title':
        category = "title"
    elif order_by == 'Message':
        category = "message"
    elif order_by == 'Number of Views':
        category = "view_number"
    
    cursor.execute("""
    DROP TABLE IF EXISTS temp_db;
    SELECT * INTO temp_db FROM %(db)s;
    ALTER TABLE temp_db DROP COLUMN id
    ALTER TABLE temp_db DROP COLUMN image;
    ORDER BY %(category)s %(order)s;
    """,
        {'db': database_name, 'category': category, 'order': order})
    sorted_data = cursor.fetchall()
    return sorted_data


### ????? util ??? ###
def convert_time(data):
    for i in data:
        ts = float(i["submission_time"])
        i["submission_time"] = time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))
    return data


@database_common.connection_handler
def update_question(cursor, edited_question: dict):
    cursor.execute("""
    UPDATE question 
    SET submission_time = %(sub_time)s
    SET view_number = %(view)s
    SET vote_number = %(vote)s
    SET title = %(title)s
    SET message = %(message)s
    SET image = %(image)s
    WHERE id = %(id)s;
    """,
        {'id': edited_question['id'], 'sub_time': edited_question['submission_time'], 
        'view': edited_question['view_number'],'vote': edited_question['vote_number'], 
        'title': edited_question['title'], 'message': edited_question['message'], 'image': edited_question['image']})


@database_common.connection_handler
def delete_question(cursor, question: dict):
    cursor.execute("""
    DELETE FROM question WHERE id = %(id)s;
    """,
        {'id': question['id']})
    delete_answers_by_question_id(question)


@database_common.connection_handler
def delete_answers_by_question_id(cursor, question: dict):
    cursor.execute("""
    DELETE FROM answer WHERE question_id = %(q_id)s;
    """,
        {'q_id': question['id']})


@database_common.connection_handler
def delete_answer(cursor, question_id, answer_id):
    cursor.execute("""
    DELETE FROM answer WHERE question_id = %(q_id)s AND id = %(a_id)s;
    """,
        {'q_id': question_id, 'a_id': answer_id})