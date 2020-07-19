# library imports

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# engine creation
engine = create_engine(
    "mssql+pyodbc://LAPTOP-MBF2NABO\\SQLEXPRESS/CreditManagement?driver=SQL+Server+Native+Client+11.0",
    convert_unicode=True,
)

# Mapping
Base = automap_base()
Base.prepare(engine, reflect=True)

User = Base.classes.Users


# app definition
app = Flask(__name__)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# User Route
@app.route('/users')
def users():

    ssn = Session(engine)
    data1 = ssn.query(User).all()
    user_list = []
    for i in data1:
        d = {
            "Name": i.Name,
            "CreditPoint": i.Credit,
            "UserId": i.UserId
        }
        user_list.append(d)
      
    return render_template('users.html',  user_list=user_list, uid=1)

# User Details Route
@app.route('/userdetails/<uid>', methods=['GET', 'POST'])
def userdetails(uid):
    msg = " "
    ssn = Session(engine)

    users = []
    user_list = ssn.query(User).all()
    if user_list:
        for user in user_list:
            dd = {
                "Name": user.Name,
                "UserId": user.UserId
            }
            
            if int(uid) != int(dd['UserId']):
                users.append(dd)

    data1 = ssn.query(User).filter_by(UserId=uid).first()
    user_list1 = []
    if data1:
        d = {
                "Name": data1.Name,
                "Email":data1.Email,
                "Phone":data1.Phone,
                "PAN":data1.PAN,
                "Curent CreditPoint": data1.Credit
            }
        
        user_list1.append(d)

    return render_template('userdetails.html', user_list1 = user_list1, users=users, uid=uid, msg=msg)

# creditdetails Route
@app.route('/creditdetails/<uid>', methods=['GET', 'POST'])
def creditdetails(uid):
    msg = ""
    status = ""
    users_data = ""
    if request.method == 'POST':
            name = request.form['username']
            credit_amount = request.form['credit']
          
            ssn = Session(engine)
            data1 = ssn.query(User).filter_by(UserId=uid).first()

            
            user_data = ssn.query(User).filter_by(Name=name.strip()).first()
            

            if user_data:
                if int(data1.Credit) >= int(credit_amount):
                    data1.Credit = int(data1.Credit)-int(credit_amount)
                    user_data.Credit = int(user_data.Credit)+int(credit_amount)

                    ssn.commit()
                    msg = f"Success!{credit_amount}credits have been sent to {name} "
                    status = True

                else:
                    msg = "Failed!"
                    status = False

            user_details = ssn.query(User).all()
            users_data = []
            for user in user_details:
                d = {
                    "Name": user.Name,
                    "CreditPoint": user.Credit,
                    "UserId": user.UserId
                }
                users_data.append(d)
    return render_template('creditdetails.html', msg=msg, status = status, users=users_data, uid=uid)


if __name__ == '__main__':
    app.run()
