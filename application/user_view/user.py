from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.main_db.db import *
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



user = Blueprint("user", __name__)
guard.init_app(app, User)


class User_schema(ma.Schema):
    class Meta:
        fields=("id","firstname","lastname","about","email","username","hashed_password",
                "roles","city","country","address","phone","created_date","school_name",
            "account_status","photo","picture","is_active","description","user_name","close","close_at",
            "status","reason","answer","user_id","ticket_id"
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
# @flask_praetorian.auth_required
def register():
   
    firstname =request.json["firstname"]
    username = request.json["username"]
    password = request.json["password"]
    lastname =request.json["lastname"]
 

    email = request.json["email"]
    picture = request.json["Picture"]
    # usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # sch =  School.query.filter_by(school_name=usr.school_name).first()
    
    
    # school_name = sch.school_name
    # address = request.json["address"]

    

    # state=request.json["state"]
     
 
    # gender=request.json["gender"]
    photo=request.json["photo"]
    


    role = request.json["role"]
    # phone = request.json["phone"]
    # confirm_password= request.json["confirm_password"]
    hashed_password= guard.hash_password(password)
    # if password == confirm_password:
    usr = User(firstname=firstname,lastname=lastname
                    ,username=username,hashed_password=hashed_password,roles=role,
                    email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),picture=picture
                 \
               
                    )
    
    db.session.add(usr)
    db.session.commit()
    db.session.close()
    resp = jsonify ("success")
    resp.status_code =200

    return resp



@user.route('/get_signin_client',methods=['GET','POST'] )
#@flask_praetorian.auth_required

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
    # user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    # acd=Academic.query.filter_by(school_name=user.school_name).first()
    # if(int(acd.countdown)<0):
    #     user.is_active = False
    #     db.session.commit()
    
    info = db.session.query(User).filter_by(id=flask_praetorian.current_user().id).all()
    results =user_schema.dump(info)
    return jsonify(results)



@user.route("/find_expired",methods=['POST'])
# @flask_praetorian.auth_required
def find_expired():
    # user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    # acd=Academic.query.filter_by(school_name=user.school_name).first()
    # if(int(acd.countdown)<0):
    #     user.is_active = False
    #     db.session.commit()
    username = request.json["username"]
    info = db.session.query(User).filter_by(username=username).all()
    results =user_schema.dump(info)
    return jsonify(results)



@user.route("/get_users",methods=['GET'])
@flask_praetorian.auth_required
def get_users():
    info = User.query.all()
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
            # user.about =request.json["about"]
            user.lastname =request.json["lastname"]
            
            # picture = request.json["picture"]
            # if picture is None:
            #     user.picture= user.picture
            # else:
            #      user.picture = picture
                 
            if password is None :
                 user.password = user.password
           
            # user.username = request.json["username"]
            else:
                 password = request.json["password"]
            # user.country = request.json["country"]
            # user.city =  request.json["city"]
            # user.address = request.json["address"]
            user.email = request.json["email"]
            user.roles =  request.json["role"]
         
    
    
     
            # user.gender=request.json["gender"]
            # user.photo=request.json["photo"]
           
            user.hashed_password =  guard.hash_password(password)
            db.session.commit()
            res = jsonify("sucess")
            res.status_code=201
            return res





@user.route("/add-ticket", methods=['GET', 'POST'])
@flask_praetorian.auth_required
def add_ticket():
    # Get form values
    reason = request.json.get('reason')
    description = request.json.get('description')
    user_id = flask_praetorian.current_user().id
    # user_email = flask_praetorian.current_user().email  # Assuming the user model has an email field

    # Validate form data
    if not reason or not description:
        return jsonify({"error": "Reason and description are required"}), 400

    # Create new ticket
    ticket = Ticket(
        reason=reason,
        description=description,
        user_id=user_id,
        status="Pending",
        created_date=datetime.now().strftime('%Y-%m-%d')
    )

    # Save to the database
    db.session.add(ticket)
    db.session.commit()

    # Get the last ticket of the current user (just created)
    last_ticket = Ticket.query.filter_by(user_id=user_id).order_by(Ticket.id.desc()).first()

    # Send email notification
    msg = Message(
        subject="New Ticket Created",
        # sender=user_email,  # User's email as the sender
        recipients=["kevinfiadzeawu@gmail.com"]  # Static recipient
    )
    msg.body = f"""
    New support ticket created by user ID: {user_id}

    Ticket Details:
    - Ticket ID: {last_ticket.id}
    - Reason: {last_ticket.reason}
    - Description: {last_ticket.description}
    - Status: {last_ticket.status}
    - Created Date: {last_ticket.created_date}

    Please address this ticket at your earliest convenience.

    Best regards,
    Support System
    """
    mail.send(msg)

    # Prepare JSON response
    response = user_schema.dump(last_ticket)
    return jsonify(response)


    # If method is GET, render the ticket creation form
    


@user.route("/tickets")
@flask_praetorian.auth_required
def tickets():

    tickets= Ticket.query.filter_by(user_id=flask_praetorian.current_user().id).order_by(Ticket.id.desc())
    result = user_schema.dump(tickets)
    return jsonify(result)





@user.route("/all_tickets")
@flask_praetorian.auth_required
def all_tickets():

    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    result = user_schema.dump(tickets)
    return jsonify(result)


@user.route("/add-answer/", methods=['GET', 'POST'])
@flask_praetorian.auth_required
def add_answer():
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first
        id = request.json["id"]
        ticket = Ticket.query.filter_by(id=id).first()
        answer_text = request.json["answer"]


        # Create new answer
        ans = Answer(
            answer=answer_text,
            ticket_id=id,
            user_name=user.username,
            created_date=datetime.now().strftime('%Y-%m-%d')
        )
        db.session.add(ans)
        ticket.status="open"
        db.session.commit()

        resp = jsonify("success")
        resp.status_code=200
        return resp



@user.route("/view-ticket/<id>", methods=['GET', 'POST'])
@flask_praetorian.auth_required
def view_ticket(id):
    ticket = Ticket.query.filter_by(id=id).all()
    result = user_schema.dump(ticket)
    return jsonify(result)
   
    


@user.route("/close_ticket",methods=["PUT","GET"])
@flask_praetorian.auth_required
def close_ticket():  # Add 'id' to function parameter
    request.json["id"]
    ticket = Ticket.query.filter_by(id=id).first()
    ticket.close = "yes"
    ticket.close_at = datetime.now().strftime('%Y-%m-%d')
    ticket.status="closed"
    db.session.commit()
    resp = jsonify("success")
    resp.status_code =200
    return resp
