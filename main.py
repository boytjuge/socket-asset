from flask import Flask, render_template, jsonify,json
from flask_socketio import SocketIO, emit
import random as rd
import mysql.connector 



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

mydb = mysql.connector.connect(
  host="10.131.13.131",
  user="reports",
  password="reports",
  database="bkn_queue"
)
@app.route('/')
def index():
    name = rd.randint(0,9)
    return render_template('index.html',name=name)


@app.route('/queue-dashboard')
def dashboard():
    name = rd.randint(0,9)
    return render_template('dashboard.html',name=name)    




@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    emit('response', {'data': message},broadcast=True)


@socketio.on('queue')
def handle_message_dash(message):
    try:
        json_data = json.loads(message)
        print(f"Received message: {json_data}")
        res_finq = getfin_q(json_data['floor'],json_data['counter'])
        res_pharq = getphar_q(json_data['floor'],json_data['counter'])
        emit('dashboard', {'data': json_data, 'queue': {'finq': res_finq , 'pharq': res_pharq}}, broadcast=True)
    except Exception as e:
        print(f"Error handling 'queue' event: {str(e)}")

@socketio.on('connect')
def handle_connect():
   
    print('Client connected')

@socketio.on('user_connected')
def handle_user_connected(message):
    print(f"User connected message: {message}")
    emit('dashboard', {'data': message},broadcast=True)



def getphar_q(floor , counter):
    mycursor = mydb.cursor()
    sql = f"SELECT RIGHT(en,4)  as queue_no ,date_ , counter, floor FROM pharq_status  WHERE  floor = '{floor}' and counter = '{counter}' AND  statusflag = 'A'  AND `status` = 'C'  AND DATE (date_)= DATE (now())  ORDER BY uid DESC 	LIMIT 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult


def getfin_q(floor , counter):
    mycursor = mydb.cursor()
    sql = f"SELECT RIGHT(en,4)  as queue_no ,date_ , counter , floor FROM finq_status  WHERE  floor = '{floor}' and counter = '{counter}' AND  statusflag = 'A'  AND `status` = 'C'  AND DATE (date_)= DATE (now())  ORDER BY uid DESC 	LIMIT 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult

if __name__ == '__main__':
    socketio.run(app,port=4099, debug=False)
