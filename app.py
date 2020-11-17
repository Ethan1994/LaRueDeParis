from flask import Flask, render_template, redirect, request, make_response
from wtform_fields import *
import models as mds
from flask_login import LoginManager, login_user
from flask_restful import Api, Resource
import os
from datetime import date, datetime
# APP
app = Flask(__name__)
app.secret_key = 'La_rue_de_paris_2020'
api = Api(app)

# database configs
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://hjffxlgqpdaftq:142f340bfcfff7f0fafad328a329282136dd3f042231cdb5fd4f4d95c7cbcb71@ec2-54-235-192-146.compute-1.amazonaws.com:5432/d6n0mqee5s1tfh'
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    Customer contact us page
    """

    def get(self):
        return make_response(render_template('contact.html', msg='Please fill out the forms'))

    def post(self):
        customer_name = request.form.get('name')
        date = str(request.form.get('date'))
        time = str(request.form.get('time'))
        guest_num = request.form.get('nums')
        # add reservation to database
        reservation_query = mds.Reservations(customer_name=customer_name, date=date, time=time, guest_num=guest_num)
        db.session.add(reservation_query)
        db.session.commit()
        db.session.close()

        return make_response(render_template('contact.html', msg='Thank you for reservation'))


class Reservations(Resource):
    """
    Admin reservation page
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
        return redirect('/admindashboard')

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
            return redirect('/admindashboard')
        else:
            return make_response(render_template("login.html", form=login_form), 200)

class Logout(Resource):
    def get(self):
        return make_response(render_template("index.html"), 200)


class Admindashboard(Resource):
    def get(self):
        return make_response(render_template("admin_dashboard.html"), 200)

class AddFood(Resource):

    def get(self):
        return make_response(render_template("add_food.html"), 200)

    def post(self):
        if 'file' not in request.files:
            msg = 'No file selected'
            return make_response(render_template("add_food.html", msg=msg), 200)
        food_cal = request.form.get('cal')
        if int(food_cal) > 5000:
            msg = 'Maximum allowed calories is 5000.'
            return make_response(render_template("add_food.html", msg=msg), 200)
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pic_src = '../static/images/' + filename
        food_name = request.form.get('name')

        food_ing = request.form.get('ingredient')
        msg = 'successfully added'

        # add food to database
        food_query = mds.Foods(food_name=food_name, food_cal=food_cal, food_ing=food_ing, pic_src=pic_src)
        db.session.add(food_query)
        db.session.commit()
        db.session.close()
        return make_response(render_template("add_food.html", msg=msg), 200)


class Delfood(Resource):

    def get(self):
        food_obj = mds.Foods.query.all()
        food_list = []

        for food in food_obj:
            food_list.append(food.food_name)

        return make_response(render_template("delete_food.html", food_list=food_list), 200)

    def post(self):
        food_name = request.form.get('food_name')
        r = db.engine.execute(f"DELETE FROM foods WHERE food_name = '{food_name}';")
        db.session.commit()
        msg = f'{food_name} Deleted'
        return make_response(render_template("delete_food.html", msg=msg), 200)


class MenuD(Resource):

    def get(self):
        food_obj = mds.Foods.query.all()
        food_list = []

        for food in food_obj:
            temp = []
            temp.append(food.food_name)
            temp.append(food.food_cal)
            temp.append(food.food_ing)
            temp.append(food.pic_src)
            food_list.append(temp)

        return make_response(render_template("menu_dynamic.html", food_list=food_list), 200)

class Reviews(Resource):

    def get(self):
        review_obj = mds.Reviews.query.all()
        reviews_list = []

        for review in review_obj:
            temp = []
            temp.append(review.name)
            temp.append(review.date)
            temp.append(review.reviews)
            reviews_list.append(temp)


        return make_response(render_template("reviews.html", reviews_list=reviews_list), 200)

    def post(self):
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        name = request.form.get('name')
        if name == '':
            name = 'Anonymous'
        reviews = request.form.get('reviews')

        if len(reviews) <= 3:
            review_obj = mds.Reviews.query.all()
            reviews_list = []

            for review in review_obj:
                temp = []
                temp.append(review.name)
                temp.append(review.date)
                temp.append(review.reviews)
                reviews_list.append(temp)
            msg = 'Review should have more than 3 letters.'
            return make_response(render_template("reviews.html", msg=msg, reviews_list=reviews_list), 200)
        # add food to database
        review_query = mds.Reviews(name=name, date=date, reviews=reviews)
        db.session.add(review_query)
        db.session.commit()
        db.session.close()
        msg = 'Thank you for your feedback.'

        review_obj = mds.Reviews.query.all()
        reviews_list = []

        for review in review_obj:
            temp = []
            temp.append(review.name)
            temp.append(review.date)
            temp.append(review.reviews)
            reviews_list.append(temp)

        return make_response(render_template("reviews.html", msg=msg, reviews_list=reviews_list), 200)

class Errors(Resource):

    @app.errorhandler(404)
    def page_not_found(e):
        # note that set the 404 status explicitly
        return ('Page not found'), 404

    @app.errorhandler(500)
    def not_logged_in(e):
        # note that set the 500 status explicitly
        return ('Server Error'), 500

    @app.errorhandler(405)
    def not_allowed(e):
        # note that set the 405 status explicitly
        return ('Method not allowed'), 405


api.add_resource(Index, "/")
api.add_resource(Menu, "/menu")
api.add_resource(MenuD, "/menud")
api.add_resource(Contact, "/contact")
api.add_resource(Reservations, "/reservations")
api.add_resource(AddFood, "/addFood")
api.add_resource(Delfood, "/delfood")
api.add_resource(Login, "/login")
api.add_resource(Admindashboard, "/admindashboard")
api.add_resource(Reviews, "/reviews")
api.add_resource(Logout, "/logout")


# app run
if __name__ == "__main__":
    app.run(debug=False)
