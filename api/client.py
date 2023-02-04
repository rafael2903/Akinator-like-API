import socketio
import threading

sio = socketio.Client()

def handle_connect():
    print('Conectado ao servidor')

def handle_question(data):
    print('Pergunta: ', data['question'])
    resposta = input('Resposta: ')
    sio.emit('answer', {'answer': int(resposta)})

def handle_disconnect():
    print('Desconectado do servidor')
    sio.disconnect()

@sio.event
def connect():
    t = threading.Thread(target=handle_connect)
    t.start()

@sio.event
def question(data):
    t = threading.Thread(target=handle_question, args=(data,))
    t.start()

@sio.event
def disconnect():
    t = threading.Thread(target=handle_disconnect)
    t.start()

sio.connect('http://localhost:5000')
sio.wait()
