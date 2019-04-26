from app.api import api


@api.route('/t1')
def hello_world():
    return 'Hello, World'
