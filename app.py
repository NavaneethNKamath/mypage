

import math
import random

import json
import re

from urllib import request, response
from flask import *
from flask import session
from flask_mail import *
from flask_bootstrap import *
from flask_session import Session
from flask_mongoengine import MongoEngine
import os
import pandas as pd




os.environ['API_USER'] = 'teamekyam@outlook.com'
os.environ['API_PASSWORD'] = 'EkyamJNN'

app = Flask(__name__)
DB_URI = "mongodb+srv://user1:EkyamJNN22@cluster0.9vdl8.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('API_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('API_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = MongoEngine()
mail = Mail(app)
db.init_app(app)
Session(app)

class Participant(db.Document):
    name = db.StringField()
    usn = db.StringField()
    branch = db.StringField()
    mobile=db.StringField()
    email = db.StringField()
    section=db.StringField()
    extra1=db.StringField()
    extra2=db.StringField()

class Flag(db.Document):
    key = db.StringField()
    value = db.StringField()
  
class User(db.Document):
    email = db.StringField()
    password = db.StringField()
    name = db.StringField()
    mobile=db.StringField()
    core=db.StringField()
    type = db.StringField(default='none')
    verified=db.StringField(default='False')
    telegram= db.StringField(default='none')
    var1=db.StringField(default='none')
    var2=db.StringField(default='none')

def generateOTP():

    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP

def sendEmail(recipientsArr,subject,msgBody):
    try:
        msg = Message(subject, sender='teamekyam@outlook.com',recipients=recipientsArr)
        msg.body = msgBody
        msg.html = msgBody
        mail.send(msg)
        return 1
    except:
        return 0

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("registerpage.html")
    else:
        if(request.form['password'] == request.form['agpassword']):
            data = {
                "name": request.form['name'].strip(),
                "email": request.form['email'].strip(),
                "mobile":request.form['mno'].strip(),
                "password": request.form['password'],
                "core":request.form['core']
                 }
            data = json.dumps(data)
            record = json.loads(data)
            d = User(name=record['name'], email=record['email'],mobile=record['mobile'],core=record['core'],password=record['password'])
            m=User.objects(email=request.form['email'])
            email=request.form['email'].strip()
            name=request.form['name'].strip()
            if m:
                for doc in m:
                    if doc['verified']=='False':
                        otp = generateOTP()
                        msg="Dear <b>%s</b>,<br>This message is sent from EKAYM web application.<br> Your OTP for confirming your registration is <b>%s</b><br> Regards. <br><b>Team EKYAM</b>" % ( name, otp)
                        if(sendEmail([email],'OTP for EKYAM Website - '+str(otp),msg)):
                            pass
                        else:
                            return render_template("registerpage.html", error="ERROR : SERVER ERROR CONTACT THE ADMIN.")
                        try:
                            m.delete()
                            d.save()
                            g=Flag.objects(key=record['email'])
                            if g:
                                g.delete()
                            m=Flag(key=record['email'],value=str(otp))
                            m.save()
                            resp = make_response(render_template("otpConfirm.html",confirm="Confirm your account first by entering the OTP sent to your registered email - "+str(record['email']+" for any changes in the email contact the admin.")))
                            resp.set_cookie('user',record['email'])
                            return resp
                        except:
                            return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
                    else:
                        return render_template("login.html", error="ERROR : YOUR ACCOUNT EXISTS YOU CAN LOGIN.")
            else:
                otp = generateOTP()
                msg="Dear <b>%s</b>,<br>This message is sent from EKAYM web application.<br> Your OTP for confirming your registration is <b>%s</b><br> Regards. <br><b>Team EKYAM</b>" % ( name, otp)
                if(sendEmail([email],'OTP for EKYAM Website - '+str(otp),msg)):
                    pass
                else:
                    return render_template("registerpage.html", error="ERROR : SERVER ERROR CONTACT THE ADMIN.")
                try:
                    d.save()
                    m=Flag(key=record['email'],value=str(otp))
                    m.save()
                    resp = make_response(render_template("otpConfirm.html"))
                    resp.set_cookie('user',record['email'])
                    return resp
                except:
                    return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
        else:
            return render_template("registerpage.html", error="ERROR : PASSWORD MISMATCH.")
@app.route('/confirmOTP',methods=['GET','POST'])
def otpConfirm():
    otpf=request.form['otp']
    try:
        otp1=Flag.objects(key=request.cookies.get('user'))
        m=json.dumps(otp1)
        m=m[1:len(m)-1]
        s=json.loads(m)
        otp=str(s['value'])
        d=User.objects(email=request.cookies.get('user'))
        if(otp==str(otpf)):
            d.update(verified="True")
            otp1.delete()
            return render_template("login.html", done="SUCCESS : ACCOUNT CREATED.")
        else:
            d.delete()
            otp1.delete()
            return render_template("registerpage.html", error="ERROR : OTP MISMATCH REGISTER AGAIN.")
    except:
        return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        
        u = User.objects(email=username)
        
        if not u:
            return render_template("login.html",error="ERROR : USER ACCOUNT DOESN'T EXIST.")
        else:
            m=json.dumps(u)
            m=m[1:len(m)-1]
            s=json.loads(m)
            if(password == s['password']):
                resp = make_response(redirect('/dataadd'))
                name = s['name']
                email = s['type']
                resp.set_cookie('user', name)
                resp.set_cookie('type', email)
                session["name"]=name
                return resp
            else:
                return render_template("login.html", error="ERROR : WRONG PASSWORD.")     
            '''if(password == s['password'] and s['type']=='ADMIN'):
                resp = make_response(redirect('/confirmUser'))
                name = s['name']
                type = s['type']
                resp.set_cookie('user', name)
                resp.set_cookie('type', type)
                resp.set_cookie('email',s['email'])
                session["name"]=name
                return resp'''
@app.route('/forgotPass',methods=['GET','POST'])
def forgotPass():
    if request.method=="GET":
        return render_template("forgotPass.html")
    else:
        email=str(request.form['email'].strip())
        otp = generateOTP()
        msg="Dear <b>%s</b>,<br>This message is sent from EKAYM web application.<br> Your OTP for confirming your identity is <b>%s</b><br> Regards. <br><b>Team EKYAM</b>" % ( name, otp)
        if(sendEmail([email],'OTP for EKYAM Website - '+str(otp),msg)):
            pass
        else:
            return render_template("registerpage.html", error="ERROR : SERVER ERROR CONTACT THE ADMIN.")
        try:
            d=Flag.objects(key=email)
            if(d):
                d.delete()
            m=Flag(key=record['email'],value=str(otp))
            m.save()
            resp = make_response(render_template("otpConfirm.html"))
            resp.set_cookie('user',record['email'])
            return resp
        except:
            return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
        

                  






@app.route('/', methods=['GET', 'POST'])
def participantlogin():
    return render_template("home.html")
    '''if request.method == "GET":
        return render_template("confirm.html",confirm=0)
    if request.method == "POST":
        adm = request.form['adm'].strip()
        mno = request.form['mno'].strip()
        
        
        u = Student.objects(usn=adm).first()
        
        
        name=u['name']
        
        if not u:
            return render_template("confirm.html",error="ERROR : STUDENT DATA DOESN'T EXIST CONTACT THE COORDINATOR.",confirm=0)
        else:
            u.update(confirm='1')
            resp = make_response(render_template( 'confirm.html', confirm=1,user=adm,Name=name))
            resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')  
            return resp
            '''

        
        
            

if __name__ == "__main__":
    app.run(debug=True)
