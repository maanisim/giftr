# Really basic program for now
#
#
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs


def createAccount():
    return


def forgotPassword():
    return


def accountLogin(username, password):
    data = {
        'username': username,
        'pass': password
    }

    with requests.Session() as session:
        post = session.post('LOGIN_URL', data=data)
        r = session.get('PAGE_URL')
        print(r.text)


url = 'test.com/login?username=test&password=thisispass'
parsed = urlparse.urlparse(url)

# URL = xxx.yyy/login?username=X&password=X
if 'login' in parsed.path:
    username = parsed.query[0]
    password = parsed.query[1]
    accountLogin(username, password)
