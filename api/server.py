import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('question', {'question': 'Do you want to continue?'})

@sio.event
def answer(sid, data):
    print('answer ', data)
    if data['answer'] == 1:
        sio.emit('question', {'question': 'Do you want to continue?'})
    elif data['answer'] == -1:
        sio.emit('question', {'question': 'Do you want to continue?'})
    elif data['answer']:
        sio.emit('question', {'question': 'invalid answer - Do you want to continue?'})

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
