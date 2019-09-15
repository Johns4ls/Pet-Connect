#Various imports
from flask import Flask, flash, render_template
app = Flask(__name__)
app.secret_key = 'some_secret'
#Initial screen upon entering website.
@app.route("/")
def index():
    user = {'username': 'Larry'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
]
    return render_template('HomePage/index.html', user = user, posts = posts)

@app.route('/login')
def login():
    return render_template('Login/login.html')
#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
