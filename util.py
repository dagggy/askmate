'''
Utility "layer" | util.py | Helper functions that can be called from any other layer,
but mainly from the business logic layer.
'''

'''
co do poprawy:
* w comment jest columna, którą nie wypełniamy - edited_count;
* nie mamy funkcjonalności do liczenia view_number (mysi się powiększać przy przejściu ze stron: /, /list, /search)
* search: nie wiadomo dlaczego po wyszukiwaniu całe wypełnienie tabeli wychodzi na .lower();
* search: nie zaimplementowana część z podżwietlaniem w odpowiedziach 
* brak zabezpieczenia w wypadkudodawania recordu o tej samej treści 
* brak wyświetlania obrazku w opcjii "edit question"
* nie wyświetla się więcej niż 1 komentarz do odpowiedzi
'''
import database_common, data_manager


ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'bmp', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@database_common.connection_handler
def get_next_id(cursor, table_name):
    cursor.execute(f"""SELECT MAX(id) FROM {table_name };""")
    return cursor.fetchall()[0]['max'] + 1

def add_apostrophe(message):
    my_string = ""
    for element in message:
        if element == "'":
            my_string += "''"
        else:
            my_string += element
    message = my_string
    return message

def voting_and_rep_user_update(add, id, add_rep, table_to_update):
    if add == -1:
        user_id = data_manager.get_user_id_by_answer_id(id)['user_id']
        if user_id is not None:
            data_manager.change_user_rep_value(user_id, -2)
    if add == 1:
        user_id = data_manager.get_user_id_by_answer_id(id)['user_id']
        if user_id is not None:
            data_manager.change_user_rep_value(user_id, add_rep)
    data_manager.update_record(id, {'vote_number': add}, table_to_update)


def convert_time_to_readable(list_of_data):
    for data in list_of_data:
        data['submission_time'] = data['submission_time'].replace(microsecond=0)
    return list_of_data


def get_all_comments_to_answer(answers_data_base, question_id):
    comments_to_answer = []
    for answer in answers_data_base:
        comment_to_answer = data_manager.get_records_by_foreign_key({'answer_id': answer['id']}, 'comment')
        if comment_to_answer != []:
            comments_to_answer.append(comment_to_answer)
    list_of_tags = []
    list_of_tag_id = data_manager.get_records_by_foreign_key({'question_id': question_id}, 'question_tag',
                                                             statement='tag_id')
    for tag_id in list_of_tag_id:
        list_of_tags.append([data_manager.get_records_by_foreign_key({'id': tag_id['tag_id']}, 'tag', statement='name'),tag_id['tag_id']])
    return list_of_tags, comments_to_answer


def get_image(question):
    try:
        image = question['image']
    except:
        image = 'NULL'
    return image


def acceptation_answer(users, user_login_in_session, question, accept_answer):
    for realdict in users:
        if user_login_in_session == realdict['login'] and realdict['id'] == question['user_id']:
            accept_answer = True
    return accept_answer


def rep_user_update_after_acceptation_answer(question_id, answer_id, accept):
    if accept == True:
        accepted_answer_id = data_manager.get_current_accepted_answer(question_id)['accepted_answer']
        if accepted_answer_id is not None:
            user_id = data_manager.get_user_id_by_answer_id(accepted_answer_id)['user_id']
            if user_id is not None:
                data_manager.change_user_rep_value(user_id, -15)
        data_manager.add_accepted_answer_to_question_bd(answer_id, question_id)
        user_id = data_manager.get_user_id_by_answer_id(answer_id)['user_id']
        if user_id is not None:
            data_manager.change_user_rep_value(user_id, 15)
    if accept == False:
        accepted_answer_id = data_manager.get_current_accepted_answer(question_id)
        user_id = data_manager.get_user_id_by_answer_id(accepted_answer_id['accepted_answer'])['user_id']
        data_manager.add_accepted_answer_to_question_bd("NULL", question_id)
        if user_id is not None:
            data_manager.change_user_rep_value(user_id, -15)