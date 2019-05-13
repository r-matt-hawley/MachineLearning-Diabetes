from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib
from urllib.parse import urlencode

CLIENT_ID = "52QRYDErEdzcipF5eAqnqgJYZZ1xJHtM"
CLIENT_SECRET = "qxxnWnXE1q00sk9c"
REDIRECT_URI = "https://t1dhighlow.herokuapp.com/login"

app = Flask(__name__, template_folder='templates')

@app.route('/')
def homepage():
    text = '<a href="%s">Click Here To Login</a>'
    return text % make_authorization_url()


def make_authorization_url():
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "offline_access"}
    url = "https://api.dexcom.com/v2/oauth2/login?" + urlencode(params)
    return url

def save_created_state(state):
    pass
def is_valid_state(state):
    return True

@app.route('/login')
def login():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    # Note: In most cases, you'll want to store the access token, in, say,
    # a session for use in other parts of your web app.
    return "Your token is: %s" % get_readings(access_token)

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
    }
    response = requests.post("https://api.dexcom.com/v2/oauth2/token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]


def get_readings(access_token):
    headers = {
        'authorization': "Bearer" + access_token}
    response = requests.get("https://api.dexcom.com/v2/users/self/egvs?startDate=?startDate=2017-01-01T00:00:00&endDate=2019-05-01T00:00:00", headers=headers)
    data_json = response.json()
    return data_json

if __name__ == '__main__':
    app.run(debug=True, port=65010)
