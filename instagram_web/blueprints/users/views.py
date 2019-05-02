from flask import Blueprint, render_template, request
from instagram_web.forms.forms import *
from models.user import *


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    # This is where I define user creation
    form = RegistrationForm(request.form)

    if form.validate():
        # Hash my password
        # Create a new instance of a user
        user = User(username=form.username.data,
                    email=form.email.data, password=password)

    return render_template('new.html', form=form)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
