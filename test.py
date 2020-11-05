# This file includes test scripts
import requests

def test_main_page():
    """
    Unit test for the main page, we test the followings:
    request returns 200 (OK) code.
    It has content
    Content type is html
    :return:
    """

    # variables for storing number of test cases
    test_cases_for_status_code = 0
    test_cases_for_content = 0

    print('starting test for main page (path "/") ...')
    for i in range(100):
        # making a call to the path
        res = requests.get('http://127.0.0.1:5000/')
        # checking the status code
        if res.status_code is not 200:
            print('Status code not 200')
        else:
            test_cases_for_status_code = test_cases_for_content + 1
        # checking the content and content type
        if str(res.headers.get('Content-Type')) != 'text/html; charset=utf-8':
            print('Error in content')
            print(str(res.headers.get('Content-Type')))
        else:
            test_cases_for_content = test_cases_for_content + 1

    # printing results
    print(f'{test_cases_for_status_code} requests returned code 200 .')
    print(f'{test_cases_for_content} responses had a content type of html.')
    print('test completed for main page\n')


def test_login_page():
    """
    Unit test for the login page, we test the followings:
    request returns 200 (OK) code.
    It has content
    Content type is html
    :return:
    """

    # variables for storing number of test cases
    test_cases_for_status_code = 0
    test_cases_for_content = 0

    print('starting test for login page (path "/login") ...')
    for i in range(100):
        # making a call to the path
        res = requests.get('http://127.0.0.1:5000/login')
        # checking the status code
        if res.status_code is not 200:
            print('Status code not 200')
        else:
            test_cases_for_status_code = test_cases_for_content + 1
        # checking the content and content type
        if str(res.headers.get('Content-Type')) != 'text/html; charset=utf-8':
            print('Error in content')
            print(str(res.headers.get('Content-Type')))
        else:
            test_cases_for_content = test_cases_for_content + 1

    # printing results
    print(f'{test_cases_for_status_code} requests returned code 200 .')
    print(f'{test_cases_for_content} responses had a content type of html.')
    print('test completed for main page\n')

def test_contact_page():
    """
    Unit test for the contact page, we test the followings:
    request returns 200 (OK) code.
    It has content
    Content type is html
    :return:
    """

    # variables for storing number of test cases
    test_cases_for_status_code = 0
    test_cases_for_content = 0

    print('starting test for contact page (path "/contact") ...')
    for i in range(100):
        # making a call to the path
        res = requests.get('http://127.0.0.1:5000/contact')
        # checking the status code
        if res.status_code is not 200:
            print('Status code not 200')
        else:
            test_cases_for_status_code = test_cases_for_content + 1
        # checking the content and content type
        if str(res.headers.get('Content-Type')) != 'text/html; charset=utf-8':
            print('Error in content')
            print(str(res.headers.get('Content-Type')))
        else:
            test_cases_for_content = test_cases_for_content + 1

    # printing results
    print(f'{test_cases_for_status_code} requests returned code 200 .')
    print(f'{test_cases_for_content} responses had a content type of html.')
    print('test completed for contact\n')



def test_menu_page():
    """
    Unit test for the menu page, we test the followings:
    request returns 200 (OK) code.
    It has content
    Content type is html
    :return:
    """

    # variables for storing number of test cases
    test_cases_for_status_code = 0
    test_cases_for_content = 0

    print('starting test for contact page (path "/menu") ...')
    for i in range(100):
        # making a call to the path
        res = requests.get('http://127.0.0.1:5000/menu')
        # checking the status code
        if res.status_code is not 200:
            print('Status code not 200')
        else:
            test_cases_for_status_code = test_cases_for_content + 1
        # checking the content and content type
        if str(res.headers.get('Content-Type')) != 'text/html; charset=utf-8':
            print('Error in content')
            print(str(res.headers.get('Content-Type')))
        else:
            test_cases_for_content = test_cases_for_content + 1

    # printing results
    print(f'{test_cases_for_status_code} requests returned code 200 .')
    print(f'{test_cases_for_content} responses had a content type of html.')
    print('test completed for menu\n')

