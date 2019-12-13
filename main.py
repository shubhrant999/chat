from flask import Flask, render_template, session, request
from flask_socketio import SocketIO
from flask_socketio import send, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/chat/<user_id>')
def chat(user_id):
    session['user'] = user_id 
    return render_template('chat.html')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        if request.form['password'] == 'Admin':
            username = request.form['username']
            return chat(username)
        else:
            return 'Wrong Credentials.'
    




@app.route('/admin')
def client():
    return render_template('admin.html')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)    
    send(room + ' has entered the room.', room=room)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):    
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # https://github.com/mnlightstone/Chatroom-Flask-Socketio/blob/master/app.py
    # https://gist.github.com/crtr0/2896891