from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from wtform_fields import *
import models as mds
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, logout_user
import requests
from clarifai.errors import ApiError
import uuid
from datetime import date
from flask_restful import Api, Resource

# APP
app = Flask(__name__)
app.secret_key = 'La_rue_de_paris_2020'
api = Api(app)

# database configs
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://dlbitpfjtupjle:c2c6671fc8c6b7ba73de945de2131b6ec73301b32fee773860c11165f4d2ab43@ec2-54-159-138-67.compute-1.amazonaws.com:5432/d4okbpcpq1i0rb'
db = mds.SQLAlchemy(app)

# app configs
login = LoginManager()
login.init_app(app)


# load the current user
@login.user_loader
def load_user(user_id):
    return mds.User.query.get(int(user_id))


class Index(Resource):
    """
    main page
    """

    def get(self):
        return make_response(render_template("index.html"))


class Menu(Resource):
    """
    Menu Page
    """

    def get(self):
        return make_response(render_template("menu.html"))


class Contact(Resource):
    """
    Contact us page
    """

    def get(self):
        return make_response(render_template('contact.html', msg='Please fill out the forms'))

    def post(self):
        customer_name = request.form.get('name')
        date = str(request.form.get('date'))
        time = str(request.form.get('time'))
        guest_num = request.form.get('nums')
        # add quiz_id and quiz_json to database
        reservation_query = mds.Reservations(customer_name=customer_name, date=date, time=time, guest_num=guest_num)
        db.session.add(reservation_query)
        db.session.commit()
        db.session.close()

        return make_response(render_template('contact.html', msg='Thank you for reservation'))


class Reservations(Resource):
    """
    Reservation page
    """

    def get(self):
        guests = mds.Reservations.query.all()
        return make_response(render_template("reservations.html", guests=guests))

    def post(self):
        guests = mds.Reservations.query.all()
        return make_response(render_template("reservations.html", guests=guests))

class Login(Resource):
    """
    Login Form Page
    """

    def validate_login(self):
        # Define Login form
        login_form = LoginForm()

        # Validating login form
        if login_form.validate_on_submit():
            user_object = mds.User.query.filter_by(username=login_form.username.data).first()
            login_user(user_object)
        return redirect('/reservations')

    def get(self):
        # Define Login form
        login_form = LoginForm()
        return make_response(render_template("login.html", form=login_form), 200)

    def post(self):
        # Define Login form
        login_form = LoginForm()

        # Validating login form
        if login_form.validate_on_submit():
            user_object = mds.User.query.filter_by(username=login_form.username.data).first()
            login_user(user_object)
        return redirect('/reservations')



class Errors(Resource):

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return ('Page not found'), 404

    @app.errorhandler(500)
    def not_logged_in(e):
        # note that we set the 404 status explicitly
        return ('Server Error'), 500

    @app.errorhandler(405)
    def not_allowed(e):
        # note that we set the 404 status explicitly
        return ('Method not allowed'), 405



api.add_resource(Index, "/")
api.add_resource(Menu, "/menu")
api.add_resource(Contact, "/contact")
api.add_resource(Reservations, "/reservations")
api.add_resource(Login, "/login")




# app run
if __name__ == "__main__":
    app.run(debug=True)
