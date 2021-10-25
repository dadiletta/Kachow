# Import WSGI server from Gevent
from gevent.pywsgi import WSGIServer

import logging, os

from app import create_app # load my app factory

app = create_app() # triggers app factory


#################
#### LOGGING 
#################
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
root_path = str(os.path.abspath((os.path.dirname(__file__))))
handler = logging.FileHandler(root_path + '/errors.log', mode='a', encoding=None, delay=False)  # errors logged to this file
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)  # attach the handler to the app's logger
app.logger.info('App started.')


# if I talk to my app through CLI, pre-load some stuff
@app.shell_context_processor
def make_shell_context():
    pass

'''
# to avoid reload issues on CSS updates
# http://flask.pocoo.org/snippets/40/
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
'''



if __name__ == '__main__':
    # Create WSGI server with params for Repl.it (IP 0.0.0.0, port 8080)
    # for our Flask app
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    # Start WSGI server
    http_server.serve_forever()
