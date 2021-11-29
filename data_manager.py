'''
This is the layer between the server and the data.
Functions here are called from server.py
and use generic functions from connection.py.
'''
from datetime import datetime
import connection
import time


def add_vote(id, add, answers_data_base):
    for dict in answers_data_base:
        if dict['id'] == id:
            dict['vote_number'] = str(int(dict['vote_number']) + add)
        dict['submission_time'] = str(time.mktime(datetime.strptime(dict['submission_time'], "%Y-%m-%d %H:%M").timetuple()))
    return answers_data_base


def get_question_by_id_number(question_id):
    database_path=connection.get_path("sample_data/question.csv")
    database = connection.read_file(database_path)
    is_question_exist = False
    for row in database:
        if row['id'] == question_id:
            is_question_exist = True
            return row
    if not is_question_exist:
        raise Exception('There is no question found with id {} in database'.format(question_id))


def get_answer_by_question_id(question_id):
    database_path=connection.get_path("sample_data/answer.csv")
    database = connection.read_file(database_path)
    answers_list = []
    for row in database:
        if row['question_id'] == question_id:
            answers_list.append(row)
    if answers_list is None:
        raise Exception('There is no answer found with question id {} in database'.format(question_id))
    else:
        return answers_list


def ask_question_answer(question, database_path):
    database = connection.read_file(database_path)
    database.append(question)
    connection.save_file(database, database_path)


def ask_question(question):
    database_path=connection.get_path("sample_data/question.csv")
    database = connection.read_file(database_path)
    database.append(question)
    file_name = "sample_data/question.csv"
    connection.save_file(database, file_name)


def sort_data(data, order_by, order_direction):
    if order_direction == "Ascending":
        reverse_for_sort = False
    elif order_direction == "Descending":
        reverse_for_sort = True
    elif order_direction == None:
        reverse_for_sort = False

    if order_by == "Number of Votes":
        data.sort(key=lambda x: int(x["vote_number"]), reverse=reverse_for_sort)
    elif order_by == "Chronology" or order_by == 'Submission time':
        data.sort(key=lambda x: datetime.strptime(x['submission_time'], '%Y-%m-%d %H:%M'), reverse=reverse_for_sort)
    elif order_by == "Answer length":
        data.sort(key=lambda x: len(x["message"]), reverse=reverse_for_sort)
    elif order_by == 'Title':
        data.sort(key=lambda x: x["title"], reverse=reverse_for_sort)
    elif order_by == 'Message':
        data.sort(key=lambda x: x["message"], reverse=reverse_for_sort)
    elif order_by == 'Number of Views':
        data.sort(key=lambda x: x["view_number"], reverse=reverse_for_sort)
    elif order_by == None:
        data.sort(key=lambda x: int(x["vote_number"]), reverse=True)
    return data


def convert_time(data):
    for i in data:
        ts = float(i["submission_time"])
        i["submission_time"] = time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))
    return data


def update_question(edited_question: dict):
    new_database = []
    database = connection.read_file('sample_data/question.csv')
    for question in database:
        if question["id"] == edited_question["id"]:
            for key, value in edited_question.items():
                question[key] = value
        new_database.append(question)
    connection.save_file(new_database, 'sample_data/question.csv')


def delete_question(question: dict):
    database = connection.read_file('sample_data/question.csv')
    database.remove(question)
    connection.save_file(database, 'sample_data/question.csv')
    delete_answers_by_question_id(question)


def delete_answers_by_question_id(question: dict):
    answers = connection.read_file('sample_data/answer.csv')
    to_delete = []
    for index in range(len(answers)):
        if answers[index]['question_id'] == question['id']:
            to_delete.append(answers[index])
    for item in to_delete:
        answers.remove(item)
    connection.save_file(answers, 'sample_data/answer.csv')


def delete_answer(question_id, answer_id):
    database = connection.read_file('sample_data/answer.csv')
    to_delete = []
    for answer in database:
        if answer['question_id'] == question_id and answer['id'] == answer_id:
            to_delete.append(answer)
    for item in to_delete:
        database.remove(item)
        connection.save_file(database, 'sample_data/answer.csv')