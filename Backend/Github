from flask import Flask, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'github'
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:5000/callback'
AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
USER_API_URL = 'https://api.github.com/user'

@app.route('/')
def home():
    return '<a href="/login">Login with GitHub</a>'

@app.route('/login')
def login():
    return redirect(f'{AUTHORIZE_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Error: No code provided'

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(ACCESS_TOKEN_URL, data=data, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        return 'Error: Failed to retrieve access token'

    access_token = response.json().get('access_token')
    if not access_token:
        return 'Error: Access token not found in response'

    session['access_token'] = access_token
    return redirect('/profile')

@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/login')

    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(USER_API_URL, headers=headers)
    if response.status_code != 200:
        return 'Error: Failed to retrieve user profile'

    user_data = response.json()
    return f'Hello, {user_data["login"]}! Your GitHub ID is {user_data["id"]}'

if __name__ == '__main__':
    app.run(debug=True)
