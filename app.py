from flask import Flask , render_template, request, session
#import RPi.GPIO as GPIO
from flask_mysqldb import MySQL
import pymysql
import pandas as pd
import os

app = Flask(__name__)
'''
db = pymysql.connect(
        host='localhost',
        user='root', 
        password = "",
        db='project',
        )
cursor = db.cursor()
app.secret_key = '1251'

fan = 32
light = 36

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Location of pins on physical board
GPIO.setup(fan,GPIO.OUT)
GPIO.output(fan,GPIO.HIGH)
GPIO.setup(light,GPIO.OUT)
GPIO.output(light,GPIO.HIGH)
print("Pins Set !!")
print("Please type 'flask run' in Terminal ")
'''

@app.route('/')
@app.route('/login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
	
        username = request.form['username']
        password = request.form['password']
        if(cursor.execute('SELECT * FROM tbl_admin WHERE a_username = % s AND a_password = % s', (username, password, ))):
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                msg = 'Logged in successfully !'                                # Nested loop to check admin or user
                return render_template('dashboard.html', msg = msg)

        elif(cursor.execute('SELECT * FROM tbl_user WHERE u_username = % s AND u_password = % s', (username, password, ))):
            account = cursor.fetchone()
            if account:
             session['loggedin'] = True
             msg = 'Logged in successfully !'
             return render_template('lfoff.html', msg = msg)  
          
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/user')
def user(): 
        cursor.execute("select * from tbl_user") 
        data = cursor.fetchall() #data from database 
        return render_template("user.html", value=data)
    
    
@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')

           

@app.route('/Devices')
def devices():
    return render_template('Devices.html') 

@app.route('/lfoff')
def lfoff():
	 GPIO.output(fan,GPIO.HIGH)
	 GPIO.output(light,GPIO.HIGH)
	 return render_template('lfoff.html')


@app.route('/lfon')
def lfon():
	 GPIO.output(fan,GPIO.LOW)
	 GPIO.output(light,GPIO.LOW)
	 return render_template('lfon.html')


@app.route('/lo_foff')
def lo_foff():
	    GPIO.output(fan,GPIO.HIGH)
	    GPIO.output(light,GPIO.LOW)
	    return render_template('lo_foff.html')

@app.route('/loff_fon')
def loff_fon():
	     GPIO.output(fan,GPIO.LOW)
	     GPIO.output(light,GPIO.HIGH)
	     return render_template('loff_fon.html')

@app.route('/forgot',methods=['GET','POST'])
def forgot():
    msg = ''
    if request.method == 'POST' and 'username2' in request.form and 'f_desc' in request.form:
        username = request.form['username2']
        f_desc = request.form['f_desc']
        usr_id = cursor.execute('SELECT u_id FROM tbl_user WHERE u_username = % s', (username))
        
        usr_id = cursor.fetchone()
        if usr_id:
            session['loggedin'] = True
            cursor.execute('insert into tbl_feedback(usr_id,f_desc) values(% s,% s)',(usr_id , f_desc ))
            
            db.commit() 
            msg = 'Submitted successfully !'
            return render_template('forgot.html', msg = msg)

       
        else:
            msg = 'User Does Not Exist ...!'
    return render_template('forgot.html', msg = msg)

@app.route('/feedback',methods=['GET','POST'])
def dbtbl():
    msg = ''
    try:
        os.remove("/home/ommi/Desktop/test_app/templates/sql-data.html")
    except:
        print('Error Deleting File !!!!')
    
    if request.method == 'POST' and 'username_name' in request.form:
        usernamedb = request.form['username_name']
        
        user_name = cursor.execute('select u_id from tbl_user where u_username = % s ',(usernamedb))
        user_name = cursor.fetchone()
        print(user_name)

        if user_name:
            session['loggedin'] = True
            cursor.execute('select * from tbl_feedback where usr_id = % s',(user_name))
            sql = cursor.fetchall() 
            df = pd.DataFrame(sql, columns=['feedback_id','user_id','Message'])
            df.to_html('templates/sql-data.html')
            
 
    return render_template('feedback.html')


@app.route('/sql-data',methods=['GET','POST'])
def data():
    msg = ''

    return render_template('sql-data.html', msg=msg)

