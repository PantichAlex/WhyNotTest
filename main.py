from celery import Celery
from celery.result import AsyncResult
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from redis import Redis

from time import sleep

app=Flask(__name__)
app.config['SECRET_KEY']='12345'
app.config['CELERY_BROKER_URL']='redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND']='redis://localhost:6379/0' 

celery=Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

socket=SocketIO(app)
redisCache=Redis(db=1)

@celery.task()
def summ(a,b):
    c=a+b
    sleep(10)
    return c
     

def saveTaskData(task):
    c=task.get()
    redisCache.set('c',c)
 
    
@socket.on('connect')
def connect():
            
    if(redisCache.exists('a','b')):
        if(redisCache.exists('c')):
            emit('ready')
        else:
           if(redisCache.exists('task_id')):
               task=AsyncResult(redisCache.get('task_id'))
               task.wait()
               saveTaskData(task)
               emit('ready')





@socket.on('get')
def getResults():
    if(not redisCache.exists('a','b','c')):
        emit('error', {"message": "Данных нет"})
    
    else:
        print(redisCache.get('a'))
        emit('push', {
            'a': int(redisCache.get('a')), 
            'b': int(redisCache.get('b')),
            'c': int(redisCache.get('c'))})
        redisCache.delete('a','b','c', 'task_id')

@socket.on("sum")
def sumController(data):
    try:
        a=int(data['a'])
        b=int(data['b'])
        currentTask=summ.delay(a,b)
        redisCache.set('a',a)
        redisCache.set('b',b)
        redisCache.set('task_id', currentTask.task_id)
        emit('accept', {"message":"Входные данные приняты"})
        currentTask.wait()
        saveTaskData(currentTask)
        emit('ready')
    except ValueError:
        errorDict={"message":"Входящие значения должны быть целыми числами"}
        
        emit('error', errorDict)

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    socket.run(app, host='localhost', port=8080)
