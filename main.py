from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random as rd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    name = rd.randint(0,9)
    return render_template('index.html',name=name)

@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    emit('response', {'data': message},broadcast=all)


@socketio.on('text')
def handle_message_dash(message):
    print(f"Received message: {message}")
    emit('dashboard', {'data': message},broadcast=all)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('user_connected')
def handle_user_connected(message):
    print(f"User connected message: {message}")
    emit('dashboard', {'data': message},broadcast=all)

if __name__ == '__main__':
    socketio.run(app, debug=True)
