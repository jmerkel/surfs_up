from flask import Flask
app = Flask(__name__)
@app.route('/')
@app.route('/number')
def hello_world():
    print('')
    return 'Hello world'
def myNum():
    print('1,2,3,4,5')
    return