'''
Utility "layer" | util.py | Helper functions that can be called from any other layer,
but mainly from the business logic layer.
'''

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'bmp', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
