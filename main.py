from celery import Celery
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

app=Flask(__name__)
app.config['SECRET_KEY']='12345'
app.config['CELERY_BROKER_URL']='redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND']='redis://localhost:6379/0' 

celery=Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
socket=SocketIO(app)


@celery.task()
def summ(a,b):
    result={"result":a+b}
    socket.emit('result', result)
    return result

@socket.on('connect')
def connect():
    print("connect")

@socket.on("sum")
def sumController(data):
    try:
        a=int(data['a'])
        b=int(data['b'])
        summ.delay(a,b)
        emit('accept', {"message":"accept"})
    except:
        emit('error', {"message":"values is not integer"})

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    socket.run(app, host='localhost', port=8080)
