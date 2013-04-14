from flask import Flask
from flask import request
from flask import render_template
from flask import url_for,redirect,flash
from flask import session, escape

app = Flask(__name__)


app.debug=True



@app.route('/')
def default():
      return render_template('index.html')

if __name__ == '__main__':
    app.run()
