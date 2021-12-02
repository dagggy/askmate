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
import database_common
import datetime

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'bmp', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@database_common.connection_handler
def get_next_id(cursor, table_name):
    cursor.execute(f"""SELECT MAX(id) FROM {table_name };""")
    return cursor.fetchall()[0]['max'] + 1
