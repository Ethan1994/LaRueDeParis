import unittest
from io import BytesIO

import requests
from app import app, db, login
import string
import random
import models as mds
from PIL import Image

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgres://hjffxlgqpdaftq:142f340bfcfff7f0fafad328a329282136dd3f042231cdb5fd4f4d95c7cbcb71@ec2-54-235-192-146.compute-1.amazonaws.com:5432/d6n0mqee5s1tfh'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    # check 2 day special
    def test_daily_special(self):
        res = self.app.get('/menud')
        for i in range(2):
            self.assertIn(b'Days Special', res.data)

    def test_add_food(self):
        res = self.app.post(
            '/addFood',
            data=dict(name='test_food', cal='test_cal', ingredient='test_ing',
                      file=(BytesIO(b'my file contents'), "test.jpg")),
            follow_redirects=True, content_type='multipart/form-data')
        self.assertIn(b'successfully added', res.data)

    # make sure that added food is in menu
    def test_added_food(self):
        res = self.app.get('/menud')
        self.assertIn(b'test_food', res.data)

    # make sure admin login works
    def test_admin_login(self):
        res = self.app.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)
        self.assertIn(b'Admin Dashboard', res.data)

    # make sure invalid credentials wont work
    def test_admin_login_invalid(self):
        res = self.app.post(
            '/login',
            data=dict(username='invalid', password='admin'),
            follow_redirects=True)
        self.assertIn(b'incorrect', res.data)

        res = self.app.post(
            '/login',
            data=dict(username='ADMIN', password='admin'),
            follow_redirects=True)
        self.assertIn(b'incorrect', res.data)

    # first add a food and then delete it make sure delete works fine
    def test_food_delete(self):
        self.app.post(
            '/addFood',
            data=dict(name='test_food', cal='test_cal', ingredient='test_ing',
                      file=(BytesIO(b'my file contents'), "test.jpg")),
            follow_redirects=True, content_type='multipart/form-data')
        res = self.app.post(
            '/delfood',
            data=dict(food_name='test_food'),
            follow_redirects=True)
        self.assertIn(b'Deleted', res.data)

    # make sure added food details are same as menu
    def test_added_food_details(self):
        self.app.post(
            '/addFood',
            data=dict(name='test_food', cal='500', ingredient='test_ing',
                      file=(BytesIO(b'my file contents'), "test.jpg")),
            follow_redirects=True, content_type='multipart/form-data')
        res = self.app.get('/menud')
        self.assertIn(b'test_food', res.data)
        self.assertIn(b'500', res.data)
        self.assertIn(b'test_ing', res.data)

    # makje sure cant add more than 500 cal
    def test_cal_boundaries(self):
        max_cal_minus_one = 4999
        max_cal = 5000
        max_cal_plus_one = 5001

        res = self.app.post(
            '/addFood',
            data=dict(name='test_food', cal=max_cal_minus_one, ingredient='test_ing',
                      file=(BytesIO(b'my file contents'), "test.jpg")),
            follow_redirects=True, content_type='multipart/form-data')
        self.assertIn(b'successfully added', res.data)
        self.app.post(
            '/delfood',
            data=dict(food_name='test_food'),
            follow_redirects=True)

        res = self.app.post(
            '/addFood',
            data=dict(name='test_food', cal=max_cal, ingredient='test_ing',
                      file=(BytesIO(b'my file contents'), "test.jpg")),
            follow_redirects=True, content_type='multipart/form-data')
        self.assertIn(b'successfully added', res.data)
        self.app.post(
            '/delfood',
            data=dict(food_name='test_food'),
            follow_redirects=True)

        res = self.app.post(
            '/addFood',
            data=dict(name='test_food', cal=max_cal_plus_one, ingredient='test_ing',
                      file=(BytesIO(b'my file contents'), "test.jpg")),
            follow_redirects=True, content_type='multipart/form-data')
        self.assertIn(b'Maximum allowed calories is 5000.', res.data)

    def test_reservation_valid(self):
        res = self.app.post(
            '/contact',
            data=dict(name='test_name', date='02/02/2020', time='12:00 AM', text = 'test_text'),
            follow_redirects=True)
        self.assertIn(b'Thank you for reservation', res.data)

# make sure admin can see reservations
    def test_admin_res_view(self):
        res = self.app.get('/reservations')
        self.assertIn(b'test_name', res.data)

# test review adding function
    def test_add_reviews(self):
        res = self.app.post(
            '/reviews',
            data=dict(name='test_name', reviews='test_review'),
            follow_redirects=True)
        self.assertIn(b'Thank you for your feedback.', res.data)

    def test_review_length(self):
        res = self.app.post(
            '/reviews',
            data=dict(name='test_name', reviews='1'),
            follow_redirects=True)
        self.assertIn(b'Review should have more than 3 letters.', res.data)

        res = self.app.post(
            '/reviews',
            data=dict(name='test_name', reviews='123'),
            follow_redirects=True)
        self.assertIn(b'Review should have more than 3 letters.', res.data)

        res = self.app.post(
            '/reviews',
            data=dict(name='test_name', reviews='1234'),
            follow_redirects=True)
        self.assertIn(b'Thank you for your feedback.', res.data)


    def test_admin_logout(self):
        res = self.app.get('/logout')
        self.assertIn(b'Bienvenu', res.data)
