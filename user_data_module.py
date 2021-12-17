import data_manager
import database_common
import datetime


@database_common.connection_handler
def is_email_exists(cursor, email):
    query = f"""SELECT login FROM user_data
            WHERE login='{email}';"""
    cursor.execute(query)
    email = cursor.fetchone()
    return email is not None

@database_common.connection_handler
def add_new_user(cursor, email, password):
    user_id = data_manager.get_next_id('user_data')
    user_link = f'/user/{user_id}'
    registration_date = datetime.now()
    cursor.execute(f"""
                        INSERT INTO user_data
                        VALUES('{user_id}', '{email}', '{password}', '{user_link}', '{registration_date}', '0', '0', '0', '0');
                        """)

@database_common.connection_handler
def get_users_records(cursor):
    cursor.execute(f"""
        SELECT id, login, registration_date, questions_number, answers_number, comments_number, user_reputation
        FROM user_data
        """)
    return cursor.fetchall()

@database_common.connection_handler
def get_single_user_record(cursor, user_id):
    cursor.execute(f"""
        SELECT id, login, registration_date, questions_number, answers_number, comments_number, user_reputation
        FROM user_data
        WHERE id = '{user_id}'
        """)
    return cursor.fetchone()

@database_common.connection_handler
def get_questions_written_by_user(cursor, user_id):
    cursor.execute(f"""
            SELECT id, submission_time, view_number, vote_number, title, message 
            FROM question
            WHERE user_id = '{user_id}'
            """)
    return cursor.fetchall()

@database_common.connection_handler
def get_answers_written_by_user(cursor, user_id):
    cursor.execute(f"""
            SELECT id, submission_time, vote_number,message, question_id 
            FROM answer
            WHERE user_id = '{user_id}'
            """)
    return cursor.fetchall()

@database_common.connection_handler
def get_comments_written_by_user(cursor, user_id):
    cursor.execute(f"""
            SELECT id,
                CASE
                    WHEN answer_id IS NOT NULL THEN 'answer'
                    ELSE 'question'
                    END AS attachment, submission_time, message, edited_count,
                CASE
                    WHEN question_id IS NOT NULL THEN question_id
                    ELSE (select distinct answer.question_id from comment
                            join answer on comment.answer_id = answer.id
                            where comment.user_id=3)
                    END AS question_id
            FROM comment
            WHERE user_id = '{user_id}';
            """)
    return cursor.fetchall()

@database_common.connection_handler
def get_password_by_email(cursor, email):
    cursor.execute(f"""
                        SELECT password
                        FROM user_data
                        WHERE login = '{email}'
    """)
    return cursor.fetchone()

@database_common.connection_handler
def get_user_id_by_email(cursor, email):
    cursor.execute(f"""
                        SELECT id
                        FROM user_data
                        WHERE login = '{email}'
    """)
    return cursor.fetchone()

@database_common.connection_handler
def change_user_rep_value(cursor, user_id, symbol, value):
    cursor.execute(f"""
                        UPDATE user_data
                        SET user_reputation = user_reputation {symbol} {value}
                        WHERE id = '{user_id}';
    """)
    #print(f'user {user_id} got {symbol}{value} rep')


@database_common.connection_handler
def get_all_records(cursor, table_name):
    cursor.execute(f"""
        SELECT *
        FROM {table_name}
        """)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id_by_answer_id(cursor, answer_id):
    cursor.execute(f"""
                        SELECT user_id
                        FROM answer
                        WHERE id = '{answer_id}';
    """)
    return cursor.fetchone()


@database_common.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    cursor.execute(f"""
                        SELECT user_id
                        FROM question
                        WHERE id = '{question_id}';
    """)
    return cursor.fetchone()