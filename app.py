from flask import Flask, render_template, request

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'

@app.route('/', methods=['POST', 'GET'])
def poll():
    
    return render_template('index.html')