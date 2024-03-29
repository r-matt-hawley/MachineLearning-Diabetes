from flask import Flask, abort, request, render_template
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
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)

    return get_token(code)

def get_token(code):
    payload = {'client_secret': CLIENT_SECRET,
               'client_id': CLIENT_ID,
               'code': code,
               'grant_type': "authorization_code",
               'redirect_uri': REDIRECT_URI}
    headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"}

    response = requests.post("https://api.dexcom.com/v2/oauth2/token",
                             params=payload,
                             headers=headers)
    token_json = response.json()
    return token_json

def get_data(access_token):
    import http.client

    conn = http.client.HTTPSConnection("api.dexcom.com")

    headers = {
    'authorization': "Bearer " + access_token[list(access_token.keys())[0]]}

    conn.request("GET", "/v2/users/self/egvs?startDate=2019-01-01T00:00:00&endDate=2019-03-01T00:00:00", headers=headers)

    res = conn.getresponse()
    data = res.read()
    sep = "_______________________________________________________"
    print(sep)
    print(access_token)
    print(sep)
    return print(data.decode("utf-8"))

@app.route('/login')
def login():
    return render_template('plots.html')

if __name__ == '__main__':
    app.run(debug=True, port=65010)
