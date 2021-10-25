"""
WELCOME
"""
from flask import render_template, redirect, flash, url_for, abort, request, send_from_directory, current_app
from flask_mail import Message
from slugify import slugify

# our objects
from . import views


######################
#### STATIC PAGES ####
######################
# Displays the home page.
@views.route('/')
@views.route('/index')
@views.route('/index.html')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
def index():
    return render_template('pages/index.html')
