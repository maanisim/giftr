# Really basic program for now
#
#
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs


def createAccount(name, email, password):
    return


def forgotPassword(email):
    return


def accountLogin(email, password):
    data = {
        'email': email,
        'pass': password
    }

    with requests.Session() as session:
        post = session.post('LOGIN_URL', data=data)
        r = session.get('PAGE_URL')
        print(r.text)


url = 'test.com/login?username=test&password=thisispass'
parsed = urlparse.urlparse(url)

if 'login' in parsed.path:
    email = parsed.query[0]
    password = parsed.query[1]
    accountLogin(email, password)

elif 'register' in parsed.path:
    name = parsed.query[0]
    email = parsed.query[1]
    password = parsed.query[2]
    createAccount(name, email, password)

elif 'forgot' in parsed.path:
    email = parsed.query[0]
    forgotPassword()
