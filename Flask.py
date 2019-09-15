#Various imports
from flask import Flask, flash, render_template

app = Flask(__name__)
#Initial screen upon entering website.
@app.route("/")
def index():
    return render_template('HomePage/index.html')


#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
