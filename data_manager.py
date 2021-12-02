##### get_question_bd -> get_questions_data_from_db
##### sort_data_bd  ->  get_sorted_data
##### get_question_by_id_bd , get_answer_by_id_bd  ->  get_record_by_id
##### update_answer_by_id_bd, update_question_by_id_bd, update_answer_by_vote_bd, update_question_by_vote_bd  ->  update_record
#####


from datetime import datetime
import database_common


@database_common.connection_handler
def get_sorted_data(cursor, database_name, order_by, order_direction, question_id=None):
    if question_id != None:
        condition = f"""WHERE question_id = '{question_id}'"""
    else:
        condition = ''

    if order_direction == "Ascending":
        order = 'ASC'
    elif order_direction == "Descending" or order_direction == None:
        order = 'DESC'

    if order_by == "Number of Votes" or order_by == None:
        category = "vote_number"
    elif order_by == "Chronology":
        category = 'submission_time'
    elif order_by == 'Title':
        category = "title"
    elif order_by == 'Message':
        category = "message"
    elif order_by == 'Number of Views':
        category = "view_number"

    cursor.execute(f"""
        SELECT * FROM {database_name}
        {condition}
        ORDER BY {category} {order};
    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_data_from_db(cursor, size_limit=None):
    if size_limit:
        condition = f"""ORDER BY submission_time DESC 
                        LIMIT '{size_limit}'"""
    else:
        condition = ''
    cursor.execute(f"""
        SELECT *
        FROM question
        {condition};
        """)
    return cursor.fetchall()


@database_common.connection_handler
def get_record_by_id(cursor, record_id, database_name):
    cursor.execute(f"""
            SELECT *
            FROM {database_name}
            WHERE id = '{record_id}';
            """)
    return cursor.fetchall()[0]


@database_common.connection_handler
def update_record(cursor, record_id, value, column_name, table_name):
    if type(value) == int:
        data_to_set = f"""{column_name} = {column_name} + {value}"""
    else:
        data_to_set = f"""{column_name} = '{value}'"""
    cursor.execute(f"""
                            UPDATE {table_name}
                            SET {data_to_set}
                            WHERE id = {record_id};
                            """)


@database_common.connection_handler
def update_question_by_id_bd(cursor, question_id):
    cursor.execute(f"""
                        UPDATE question
                        SET view_number = view_number + 1
                        WHERE id = '{question_id}';
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
def get_answer_by_question_id_bd(cursor, question_id):
    cursor.execute(f"""
                            SELECT  id, submission_time, vote_number, question_id, message, image
                            FROM answer
                            WHERE question_id = '{question_id}'
                            ORDER BY vote_number DESC
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
def adding_new_question_bd(cursor, title, message, image):
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
def delete_answer_by_id_bd(cursor, question_id, answer_id):
    cursor.execute(f"""
                        DELETE FROM answer 
                        WHERE id = '{answer_id}' and question_id = '{question_id}'
                        """)


@database_common.connection_handler
def adding_new_comment_to_question_bd(cursor, message, question_id):
    current_id = max_id_comment_bd()[0]['max'] + 1
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO comment
                    VALUES('{current_id}', '{question_id}', NULL , '{message}', '{current_time}', NULL);
                    """)


@database_common.connection_handler
def adding_new_comment_to_answer_bd(cursor, message, answer_id):
    current_id = max_id_comment_bd()[0]['max'] + 1
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO comment
                    VALUES('{current_id}', NULL ,'{answer_id}', '{message}', '{current_time}', NULL);
                    """)


@database_common.connection_handler
def max_id_comment_bd(cursor):
    cursor.execute("""SELECT MAX(id) FROM comment""")
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_question_id_bd(cursor, question_id):
    cursor.execute(f"""
                            SELECT *
                            FROM comment
                            WHERE question_id = '{question_id}'
                            """)
    return cursor.fetchall()

@database_common.connection_handler
def search_by_phrase(cursor,phrase):
    cursor.execute(f"""
                    SELECT DISTINCT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message
                    FROM question
                    LEFT OUTER JOIN answer
                    ON question.id=answer.question_id
                    WHERE LOWER(CONCAT(question.title, question.message, answer.message)) 
                    LIKE '%{phrase}%';
                    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_answer_id_bd(cursor, answer_id):
    cursor.execute(f"""
                        SELECT *
                        FROM comment
                        WHERE answer_id = '{answer_id}'
                        """)
    return cursor.fetchall()


@database_common.connection_handler
def adding_new_tag_bd(cursor, new_tag):
    current_id = max_id_tag_bd()[0]['max'] + 1
    cursor.execute(f"""
                        INSERT INTO tag
                        VALUES('{current_id}', '{new_tag}');
                        """)


@database_common.connection_handler
def max_id_tag_bd(cursor):
    cursor.execute("""SELECT MAX(id) FROM tag""")
    return cursor.fetchall()


@database_common.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
        SELECT *
        FROM tag
        """)
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_id_by_tag_bd(cursor, tag):
    cursor.execute(f"""
                        SELECT id
                        FROM tag
                        WHERE name = '{tag}'
                        """)
    return cursor.fetchall()


@database_common.connection_handler
def add_tag_to_question_tag_bd(cursor, question_id, tag_id):
    cursor.execute(f"""
                        INSERT INTO question_tag
                        VALUES('{question_id}', '{tag_id}');
                        """)


@database_common.connection_handler
def get_tag_id_by_question_id_bd(cursor, question_id):
    cursor.execute(f"""
                        SELECT tag_id
                        FROM question_tag
                        WHERE question_id = '{question_id}'
                        """)
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_by_tag_id_bd(cursor, tag_id):
    cursor.execute(f"""
                        SELECT name
                        FROM tag
                        WHERE id = '{tag_id}'
                        """)
    return cursor.fetchall()