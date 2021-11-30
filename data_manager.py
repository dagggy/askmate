'''
This is the layer between the server and the data.
Functions here are called from server.py
and use generic functions from connection.py.
'''
from datetime import datetime
import database_common


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


@database_common.connection_handler
def get_question_bd(cursor):
    cursor.execute("""
        SELECT *
        FROM question
        """)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id_bd(cursor, question_id):
    cursor.execute(f"""
        SELECT *
        FROM question
        WHERE id = '{question_id}'
        """)
    return cursor.fetchall()


@database_common.connection_handler
def update_question_by_id_bd(cursor, question_id):
    cursor.execute(f"""
                        UPDATE question
                        SET view_number = view_number + 1
                        WHERE id = '{question_id}';
                        """)


@database_common.connection_handler
def update_answer_by_vote_bd(cursor, id, add):
    cursor.execute(f"""
                        UPDATE answer
                        SET vote_number = vote_number + {add}
                        WHERE id = '{id}';
                        """)


@database_common.connection_handler
def update_question_by_vote_bd(cursor, id, add):
    cursor.execute(f"""
                        UPDATE question
                        SET vote_number = vote_number + {add}
                        WHERE id = '{id}';
                        """)


@database_common.connection_handler
def get_answer_by_question_id_bd(cursor, question_id):
    cursor.execute(f"""
                            SELECT  id, submission_time, vote_number, question_id, message, image
                            FROM answer
                            WHERE question_id = '{question_id}'
                            """)
    return cursor.fetchall()


@database_common.connection_handler
def max_id_answer_bd(cursor):
    cursor.execute("""SELECT MAX(id) FROM answer""")
    return cursor.fetchall()


@database_common.connection_handler
def adding_new_answer_bd(cursor, question_id, message, image):
    current_id = max_id_answer_bd()[0]['max'] + 1
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO answer
                    VALUES('{current_id}', '{current_time}', '0', '{question_id}', '{message}', '{image}');
                    """)


@database_common.connection_handler
def max_id_question_bd(cursor):
    cursor.execute("""SELECT MAX(id) FROM question""")
    return cursor.fetchall()


@database_common.connection_handler
def adding_new_applicant_bd(cursor, title, message, image):
    current_id = max_id_question_bd()[0]['max'] + 1
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO question
                    VALUES('{current_id}', '{current_time}', '0', '0', '{title}', '{message}', '{image}');
                    """)


@database_common.connection_handler
def delete_question_by_id_bd(cursor, question_id):
    cursor.execute(f"""
                        DELETE FROM question 
                        WHERE id = '{question_id}'
                        """)


@database_common.connection_handler
def update_question_by_id_bd(cursor, id, title, message, image):
    current_time = datetime.now()
    cursor.execute(f"""
                        UPDATE question
                        SET vote_number = '0', view_number = '0', title = '{title}', message = '{message}', submission_time = '{current_time}', image = '{image}'
                        WHERE id = '{id}';
                        """)


@database_common.connection_handler
def delete_answer_by_id_bd(cursor, question_id, answer_id):
    cursor.execute(f"""
                        DELETE FROM answer 
                        WHERE id = '{answer_id}' and question_id = '{question_id}'
                        """)