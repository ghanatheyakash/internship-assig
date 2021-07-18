from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)
app.secret_key = 'a' 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'new'
mysql = MySQL(app)
@app.route('/')
def intro():
    return render_template('homepage.html')
@app.route('/signup',methods=['GET','POST'])
def signup():
    msg=" "
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        number= request.form['number']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM internship WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO internship VALUES (NULL, % s, % s, % s, %s)', (username, email,password,number))
            mysql.connection.commit()
            msg = 'You have successfully registered ! \n \n refer to your mail for further information'
            body=" Hello {} \n\n Welcome to Python. We're thrilled to see you here!\n We're confident that we will help you get a grasp on Python \n use these credentials to signin \n username :{}\n password : {}".format(username,username,password)
            subject="Python course"
            message=MIMEMultipart()
            message['From']="crackpython21@gmail.com"
            message['To']=email
            message['subject']=subject
            message.attach(MIMEText(body,'plain'))
            text=message.as_string()
            mail=smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.login("crackpython21@gmail.com","python@21")
            mail.sendmail("crackpython21@gmail.com",email,text)
            mail.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
            
    return render_template('homepage.html',msg=msg)   

@app.route('/login.html',methods=['GET','POST'])  
def signin():  
    
    return render_template('login.html')
    
if __name__ == '__main__':
   app.run(debug=True,port = 5000)