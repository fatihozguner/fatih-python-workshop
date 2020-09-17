# Import Flask modules
from flask import Flask, render_template, request

# Create an object named app
app = Flask(__name__)

# Create a function named `home` which uses template file named `index.html` given under `templates` folder,
# send your name as template variable, and assign route of no path ('/')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', name='Fatih')
@app.route('/greet', methods=['GET'])
def greet():
    if 'user' in request.args:
        usr = request.args['user']
        return render_template('greet.html', user=usr)
    else:
        return render_template('greet.html', user='Send your user name with "user" parameter in query string')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)