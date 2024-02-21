from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.main_db.db import User,db
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



user = Blueprint("user", __name__)
guard.init_app(app, User)


class User_schema(ma.Schema):
    class Meta:
        fields=("id","firstname","lastname","about","email","username","hashed_password",
                "roles","city","country","address","phone","created_date",
                "isa_savings","other_savings","account_status",
                    "state","transaction_pin" ,"account_number","premier_account","other_savings","photo"
)
        









user_schema=User_schema(many=True)


@user.route("/register_quick",methods=["POST"])
def register_quick():
    firstname =request.json["firstname"]
    username = request.json["username"]
    password = request.json["password"]
    lastname =request.json["lastname"]
    about = request.json["about"]
    country = request.json["country"]
    city = request.json["city"]

    email = request.json["email"]
    address = request.json["address"]


    role = "guest"
    phone = request.json["phone"]
    # confirm_password= request.json["confirm_password"]
    hashed_password= guard.hash_password(password)
    # if password == confirm_password:
    owner = User(firstname=firstname,lastname=lastname,about=about,country=country,
                    city=city ,phone=phone,username=username,hashed_password=hashed_password,roles=role,address=address,
                    email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'))
    db.session.add(owner)
    db.session.commit()
    resp = jsonify ("success")
    resp.status_code =200

    return resp






@user.route("/register",methods=["POST"])
def register():
    
    firstname =request.json["firstname"]
    username = request.json["username"]
    password = request.json["password"]
    lastname =request.json["lastname"]
    about = request.json["about"]
    country = request.json["country"]
    city = request.json["city"]

    email = request.json["email"]
    address = request.json["address"]

    
    city=request.json["city"]
     
    # state=request.json["state"]
     
 
    # gender=request.json["gender"]
    # photo=request.json["photo"]
    


    role = request.json["role"]
    phone = request.json["phone"]
    # confirm_password= request.json["confirm_password"]
    hashed_password= guard.hash_password(password)
    # if password == confirm_password:
    owner = User(firstname=firstname,lastname=lastname,about=about,country=country,
                    city=city ,phone=phone,username=username,hashed_password=hashed_password,roles=role,address=address,
                    email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
                 \
               
                    )
    
   
    resp = jsonify ("success")
    resp.status_code =200

    return resp



@user.route('/get_signin_client',methods=['GET','POST'] )
#@login_required

def get_signin_client(): 
      #user_man = User.query.all()  
      #doc_appoint = Appointments.query.filter_by(doctor_id =current_user.id).all()
      #rows = db.session.query(Appointments.doctor_id == current_user.id).count()
        req = request.get_json(force=True)
        username = req.get("username", None)
        password = req.get("password", None)
        owner= User.query.filter_by(username=username).first()
       
        
        user = guard.authenticate(username,password)
        
        ret = {"id_token": guard.encode_jwt_token(user)}


      #  print(ret)
        #resp =jsonify("success")
        return ( ret,200)


@user.route("/get_info",methods=['GET'])
@flask_praetorian.auth_required
def get_info():
    info = db.session.query(User).filter_by(id=flask_praetorian.current_user().id).all()
    results =user_schema.dump(info)
    return jsonify(results)




@user.route("/get_users",methods=['GET'])
@flask_praetorian.auth_required
def get_users():
    info = db.session.query(User).all()
    results =user_schema.dump(info)
    return jsonify(results)

@user.route("/delete_user/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_user(id):
    # id = request.json["id"]
    info = db.session.query(User).filter_by(id=id).first()
    db.session.delete(info)
    db.session.commit()
    res = jsonify("sucess")
    res.status_code=200
    return res




@user.route("/get_user_details/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_user_details(id):
    # id = request.json["id"]
    info = db.session.query(User).filter_by(id=id).all()
    results =user_schema.dump(info)
    return jsonify(results)




@user.route("/update_user_profile",methods=['PUT'])
@flask_praetorian.auth_required
def update_user_profile():
    
            id = request.json["id"]

            # firstname =request.json["firstname"]
            # about =request.json["about"]
            # lastname =request.json["lastname"]
            # phone =  request.json["phone"]
            # username = request.json["username"]
            # password = request.json["password"]
            # country = request.json["country"]
            # city =  request.json["city"]
            # address = request.json["address"]
            # email = request.json["email"]
            password = request.json["password"]

            user = User.query.filter_by(id=id).first()
            user.firstname =request.json["firstname"]
            user.about =request.json["about"]
            user.lastname =request.json["lastname"]
            user.phone =  request.json["phone"]
            user.username = request.json["username"]
            password = request.json["password"]
            user.country = request.json["country"]
            user.city =  request.json["city"]
            user.address = request.json["address"]
            user.email = request.json["email"]
            user.roles =  request.json["role"]
         
    
    
     
            # user.gender=request.json["gender"]
            # user.photo=request.json["photo"]
           
            user.hashed_password =  guard.hash_password(password)
            db.session.commit()
            res = jsonify("sucess")
            res.status_code=200
            return res

