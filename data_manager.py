from datetime import datetime
import database_common


@database_common.connection_handler
def sort_data_bd(cursor, database_name, order_by, order_direction):
    if order_direction == "Ascending" or order_direction == None:
        order = 'ASC'
    elif order_direction == "Descending":
        order = 'DESC'

    if order_by == "Number of Votes" or order_by == None:
        category = "vote_number"
    elif order_by == "Chronology" or order_by == 'Submission time':
        category = 'submission_time'
    elif order_by == "Answer length":
        category = "message"
    elif order_by == 'Title':
        category = "title"
    elif order_by == 'Message':
        category = "message"
    elif order_by == 'Number of Views':
        category = "view_number"

    cursor.execute(f"""
        DROP TABLE IF EXISTS temp_db;
        SELECT * INTO temp_db FROM question;
        ALTER TABLE temp_db DROP COLUMN image;
        ALTER TABLE temp_db DROP COLUMN id;
        SELECT * FROM temp_db
        ORDER BY {category} {order};
    """)
    sorted_data = cursor.fetchall()
    return sorted_data


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