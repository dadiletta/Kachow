"""
WELCOME: app constructor & factory - glave/app/__init__.py
"""
from flask import Flask, render_template, current_app
from werkzeug.local import LocalProxy
from flask_restful import Api

from .extensions import mail, ckeditor, moment, csrf, jwt

# relay for logger
logger = LocalProxy(lambda: current_app.logger)


def crash_page(e):
    return render_template('error_pages/500.html'), 500

def page_not_found(e):
    return render_template('error_pages/404.html'), 404

def page_forbidden(e):
    return render_template('error_pages/403.html'), 403

# sort of like an application factory
def create_app(*args): 
    # Initialize Flask and set some config values
    app = Flask(__name__)
    app.config.from_object('settings')
    
    mail.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)

    '''
    if os.environ.get('FLASK_ENV', False) != 'development':
        sentry_sdk.init(dsn="", \
                        integrations=[FlaskIntegration()])
    '''

    # BLUEPRINTS
    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)
    

    # activate API blueprint: https://stackoverflow.com/questions/38448618/using-flask-restful-as-a-blueprint-in-large-application
    jwt.init_app(app) # bolt on our Javascript Web Token tool
    from .api import api_blueprint   
    restful = Api(api_blueprint, prefix="/api/v1") 
    from .api import add_resources
    add_resources(restful)
    app.register_blueprint(api_blueprint) # registering the blueprint effectively runs init_app on the restful extension

    '''
    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return models.RevokedTokenModel.is_jti_blocklisted(jti) 
    '''
    
    # error handlers
    app.register_error_handler(500, crash_page)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_forbidden)


    # Executes before the first request is processed.
    @app.before_first_request
    def before_first_request():
        pass


    @app.before_request
    def before_request():
        pass
    
    return app
