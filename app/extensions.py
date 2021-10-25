from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
 
mail = Mail()
ckeditor = CKEditor()
moment = Moment()
csrf = CSRFProtect()
jwt = JWTManager()