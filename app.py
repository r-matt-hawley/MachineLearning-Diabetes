#imports
from flask import Flask
from uuid import uuid4
from flask import abort, request, render_template
import requests
import json
import urllib
from urllib.parse import urlencode
import random
import requests.auth

#client variables
CLIENT_ID = "52QRYDErEdzcipF5eAqnqgJYZZ1xJHtM"
CLIENT_SECRET = "qxxnWnXE1q00sk9c"
REDIRECT_URI = "https://t1dhighlow.herokuapp.com/login"

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    #text = '<a href="%s">enter authorization credentials</a>'
    return render_template('index.html', url=make_authorization_url())

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
        return "We ran into an issue with your login: " + error

    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    authorization_code = request.args.get('code')
    access_token = get_token(authorization_code)
    return get_data(access_token)

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    response = requests.post("https://api.dexcom.com/v2/oauth2/token",
                             auth=client_auth,
                             data=post_data)

    token_json = response.json()
    return token_json

def get_data(access_token):
    headers = {
    'authorization': "Bearer " + access_token[list(access_token.keys())[0]]}
    response = requests.get("https://api.dexcom.com/v2/users/self/egvs?startDate=2019-05-01T00:00:00&endDate=2019-05-11T00:00:00", headers=headers)
    me_json = response.json()
    #######################################
    sep = "__________________________________________________________"
    print(sep)
    print(access_token)
    print(sep)
    print(me_json)
    print(sep)
    #######################################

    return me_json[['unit', 'rate', 'egvs']]

@app.route('/plots')
def plots():
    return render_template('plots.html')

if __name__ == '__main__':

    port = 8000 + random.randint(0, 999)
    app.run(port=port, debug=False)
