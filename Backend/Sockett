from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread
import time

app = Flask(__name__)
socketio = SocketIO(app)

def stream_terminal_output():
    while True:
        output = shell_tool('cmde')
        socketio.emit('terminal_output', {'data': output})
        time.sleep(1) 

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    if not hasattr(socketio, 'background_thread'):
        socketio.background_thread = Thread(target=stream_terminal_output)
        socketio.background_thread.start()

if __name__ == '__main__':
    socketio.run(app)
