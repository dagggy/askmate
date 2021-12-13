'''data_manager.py
##### sort_data_bd, get_answer_by_question_id_bd, get_question_bd  ->  get_sorted_data
##### get_question_by_id_bd , get_answer_by_id_bd  ->  get_record_by_primary_key
##### get_comment_by_question_id_bd, get_comment_by_answer_id_bd, get_tag_id_by_tag_bd, get_tag_id_by_question_id_bd, get_tag_by_tag_id_bd  ->  get_records_by_foreign_key
##### update_answer_by_id_bd, update_question_by_id_bd, update_answer_by_vote_bd, update_question_by_vote_bd  ->  update_record
##### get_all_tags  -> get_all_records
##### sorting by message and title now works correctly
##### max_id_answer_bd, max_id_question_bd, max_id_comment_bd, max_id_tag_bd  ->  get_next_id
##### adding_new_answer_bd  ->  add_new_answer_record
##### adding_new_question_bd  ->  add_new_question_record
##### adding_new_comment_to_question_bd  ->  add_new_comment_to_question_record
##### adding_new_comment_to_answer_bd  ->  add_new_comment_to_answer_record
##### adding_new_tag_bd  ->  add_new_tag
templates
##### main_page.html  ->  home_page.html
'''

import database_common
from datetime import datetime
'''
NEW_RECORD = {
    'answer': "'{get_next_id('answer')}', '{datetime.now()}', 0, '{question_id}', '{message}', '{image}'",
    'question': "'{get_next_id('question')}', '{datetime.now()}', 0, 0, '{title}', '{message}', '{image}'",
    'comment': "'{get_next_id('comment')}', '{question_id}', '{answer_id}', '{message}','{datetime.now()}', '{edited_count}'",
    'tag': "'{get_next_id('tag')}', '{name}'",
    'question_tag': "'{question_id}', '{answer_id}'"
}
'''


@database_common.connection_handler
def get_sorted_data(cursor, table_name, order_by=None, order_direction=None, question_id=None):
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
        category = "LOWER(title)"
    elif order_by == 'Message':
        category = "LOWER(message)"
    elif order_by == 'Number of Views':
        category = "view_number"

    cursor.execute(f"""
        SELECT * FROM {table_name}
        {condition}
        ORDER BY {category} {order};
    """)
    return cursor.fetchall()

###############################################
@database_common.connection_handler
def get_top_records(cursor, table_name, column_name, size_limit):
    cursor.execute(f"""
        SELECT *
        FROM {table_name}
        ORDER BY {column_name} DESC 
        LIMIT {size_limit};
        """)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_records(cursor, table_name):
    cursor.execute(f"""
        SELECT *
        FROM {table_name}
        """)
    return cursor.fetchall()

##############################################
@database_common.connection_handler
def get_next_id(cursor, table_name):
    cursor.execute(f"""SELECT MAX(id) FROM {table_name };""")
    return cursor.fetchall()[0]['max'] + 1

''' Example pk_dict = {'id': 2} '''
@database_common.connection_handler
def get_record_by_primary_key(cursor, pk_dict, table_name, statement='*'):
    for column_name, value in pk_dict.items():
        cursor.execute(f"""
                SELECT {statement}
                FROM {table_name}
                WHERE {column_name} = '{value}';
                """)
    return cursor.fetchall()[0]


''' Example fk_dict = {'question_id': 12} '''
@database_common.connection_handler
def get_records_by_foreign_key(cursor, fk_dict, table_name,  statement='*'):
    for column_name, value in fk_dict.items():
        cursor.execute(f"""
                    SELECT {statement}
                    FROM {table_name}
                    WHERE {column_name} = '{value}';
                    """)
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
def get_comment_by_answer_id_bd(cursor, answer_id):
    cursor.execute(f"""
                        SELECT *
                        FROM comment
                        WHERE answer_id = '{answer_id}'
                        """)
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
def get_tag_id_by_question_id_bd(cursor, question_id):
    cursor.execute(f"""
                        SELECT tag_id
                        FROM question_tag
                        WHERE question_id = '{question_id}'
                        """)
    return cursor.fetchall()




################################################

@database_common.connection_handler
def add_new_answer_record(cursor, question_id, message, image, table_name='answer'):
    current_id = get_next_id(table_name)
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO answer
                    VALUES('{current_id}', '{current_time}', '0', '{question_id}', '{message}', '{image}');
                    """)


@database_common.connection_handler
def add_new_question_record(cursor, title, message, image, table_name='question'):
    current_id = get_next_id(table_name)
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO question
                    VALUES('{current_id}', '{current_time}', '0', '0', '{title}', '{message}', '{image}');
                    """)

@database_common.connection_handler
def add_new_comment_to_question_record(cursor, message, question_id, table_name='comment'):
    current_id = get_next_id(table_name)
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO comment
                    VALUES('{current_id}', '{question_id}', NULL , '{message}', '{current_time}', NULL);
                    """)


@database_common.connection_handler
def add_new_comment_to_answer_record(cursor, message, answer_id, table_name='comment'):
    current_id = get_next_id(table_name)
    current_time = datetime.now()
    cursor.execute(f"""
                    INSERT INTO comment
                    VALUES('{current_id}', NULL ,'{answer_id}', '{message}', '{current_time}', 0);
                    """)


@database_common.connection_handler
def add_new_tag(cursor, new_tag, table_name='tag'):
    current_id = get_next_id(table_name)
    cursor.execute(f"""
                        INSERT INTO tag
                        VALUES('{current_id}', '{new_tag}');
                        """)

@database_common.connection_handler
def add_tag_to_question_tag_bd(cursor, question_id, tag_id, table_name='question_tag'):
    cursor.execute(f"""
                        INSERT INTO {table_name}
                        VALUES('{question_id}', '{tag_id}');
                        """)



########################################################################
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
def delete_tag_from_question(cursor, question_id, tag_id):
    cursor.execute(f"""
                    DELETE FROM question_tag
                    WHERE question_id = '{question_id}' and tag_id = '{tag_id}';
    """)


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE id = '{comment_id}'
    """)


###################################################

@database_common.connection_handler
def search_by_phrase(cursor, phrase):
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
def update_comment_edited_count(cursor, id):
    cursor.execute(f"""
                        UPDATE comment
                        SET edited_count = edited_count + 1
                        WHERE id = '{id}';
                        """)


''' Example changes_dict = {'title': 'updated title', 'vote_number': 1} '''
@database_common.connection_handler
def update_record(cursor, record_id, changes_dict, table_name):
    for column_name, value in changes_dict.items():
        if type(value) == int:
            data_to_set = f"""{column_name} = {column_name} + {value}"""
        else:
            data_to_set = f"""{column_name} = '{value}'"""
        cursor.execute(f"""
                                UPDATE {table_name}
                                SET {data_to_set}
                                WHERE id = {record_id};
                                """)
###################################
###################################
###################################
@database_common.connection_handler
def get_next_user_id(cursor):
    cursor.execute(f"""SELECT MAX(user_id) FROM user_data;""")
    return cursor.fetchall()[0]['max'] + 1


@database_common.connection_handler
def add_new_user(cursor, email, password):
    user_id = get_next_user_id()
    user_link = f'/user/{user_id}'
    registration_date = datetime.now()
    cursor.execute(f"""
                        INSERT INTO user_data
                        VALUES('{user_id}', '{email}', '{password}', '{user_link}', '{registration_date}', '0', '0', '0', '0');
                        """)


@database_common.connection_handler
def is_email_exists(cursor, email):
    query = f"""SELECT login FROM user_data
            WHERE login='{email}';"""
    cursor.execute(query)
    email = cursor.fetchone()
    return email is not None


