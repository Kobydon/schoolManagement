from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.user.user_db import User,db,RoomType,Guests,Transaction,Loan,Insurance,Card
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
        



class transactionSChema(ma.Schema):
    class Meta:
        fields=("id","name","amount","type","debit_accout","account_umber","bank_name","created_date",
                "branch_name","status","branch_name"
)
        



class loanSchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","status","created_date","account_number","car","model",
                "branch_name","status","branch_name"
)
        
        
class insuranceSchema(ma.Schema):
    class Meta:
        fields=("id","name","policy_number","email","created_date","phone","address","comments",
                "branch_name","status","branch_name"
)


        
class cardSchema(ma.Schema):
    class Meta:
        fields=("id","name","card_type","card_number","pin","created_date","expiry_date","status"
)

class MessageSchema(ma.Schema):
    class Meta:
        fields=("id","message","client"
)


message_schema = MessageSchema(many=True)


card_schema= cardSchema(many=True)

loan_schema =loanSchema(many=True)
insurance_schema = insuranceSchema(many=True)


trans_schema =transactionSChema(many=True)

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
    
    gsts = Guests(first_name =firstname,last_name=lastname,email=email,address=address,city=city,username=username)
    db.session.add(owner)
    db.session.add(gsts)
    db.session.commit()
    db.session.close()
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



@user.route("/add_transaction",methods=["POST"])
@flask_praetorian.auth_required
def add_transaction():
          debit_account =request.json["debit_account"]
          amount =request.json["amount"]
          trans= Transaction(

          name =request.json["name"],
          bank_name =request.json["bank_name"],
          branch_name =request.json["branch_name"],
          transaction_pin =request.json["transaction_pin"],
          debit_accout =request.json["debit_account"],
          amount =request.json["amount"],
          account_umber =request.json["account_number"],
          status ="sucess",
          type ="debit",
          created_by_id = flask_praetorian.current_user().id ,
          created_date = datetime.now().strftime('%Y-%m-%d %H:%M'))
        
          

          user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
          if(debit_account=="premier_account"):
                user.premier_account = int(user.premier_account )- int(amount)

          if(debit_account=="isa_savings"):
                user.premier_account = int(user.isa_savings) - int(amount)

         
          if(debit_account =="other_savings"):
                user.other_savings = int(user.other_savings) - int(amount)


          db.session.add(trans)
          db.session.commit()
          resp = jsonify("success")
          resp.status_code =200
          return resp


@user.route("/get_transaction",methods=["GET"])
@flask_praetorian.auth_required
def get_transaction():
      trans = Transaction.query.filter(Transaction.created_by_id==flask_praetorian.current_user().id)
      lst = trans.order_by(desc(Transaction.created_date))
      result = trans_schema.dump(lst)
      return jsonify(result)


@user.route("/get_every_transaction",methods=["GET"])
@flask_praetorian.auth_required
def get_every_transaction():
      trans = Transaction.query.all()
    #   lst = trans.order_by(desc(Transaction.created_date))
      result = trans_schema.dump(trans)
      return jsonify(result)




@user.route("/get_transaction_detail/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_transaction_detail(id):
      trans = Transaction.query.filter_by(id=id).all()
     
      result = trans_schema.dump(trans)
      return jsonify(result)
     

          
@user.route("/get_loan",methods=["GET"])
@flask_praetorian.auth_required
def get_loan():
      loans = Loan.query.filter_by(created_by_id=flask_praetorian.current_user().id).all()
     
      result = loan_schema.dump(loans)
      return jsonify(result)
     


@user.route("/add_loan",methods=["POST"])
@flask_praetorian.auth_required
def add_loan():
    #   loans = Loan.query.filter_by(created_by_id=flask_praetorian.current_user_id().id).all()
     
        loan = Loan(
            name= request.json["name"],
            car= request.json["car"],
            model= request.json["model"],
            amount= request.json["amount"],
            account_number= request.json["account_number"],

            status= "pending",
            created_date = datetime.now().strftime('%Y-%m-%d %H:%M'),
            created_by_id = flask_praetorian.current_user().id )
         
       
        db.session.add(loan)
        db.session.commit()
        resp = jsonify("success")
        resp.status_code=200
#         return resp

# @user.route("/send_message",methods=["POST"])
# @flask_praetorian.auth_required
# def send_message():
#     #   loans = Loan.query.filter_by(created_by_id=flask_praetorian.current_user_id().id).all()
#         client= request.json["client"]
#         message= request.json["message"]
#         print(client)
#         messge = Messager(message=message,client=client)
            
#             # name= request.json["model"],

         
       
#         db.session.add(messge)
#         db.session.commit()
#         resp = jsonify("success")
#         resp.status_code=200
#         return resp
     



# @user.route("/get_message_for_client",methods=["GET"])
# @flask_praetorian.auth_required
# def get_message_for_client():
#       trans = Messager.query.filter(Message.client==flask_praetorian.current_user.username)
#       lst = trans.order_by(desc(trans.created_date))
#       result = message_schema.dump(lst)
#       return jsonify(result)







# @user.route("/delete_message",methods=["GET"])
# @flask_praetorian.auth_required
# def delete_message():
#       trans = Messager.query.filter(id=id).first()
#       db.session.dete(trans)  
#       db.session.commit()    
#       resp = jsonify("success")
#       resp.status_code=200
#       return resp






# @user.route("/get_message",methods=["GET"])
# @flask_praetorian.auth_required
# def get_message():
#       trans = Messager.query.all()
#       result = message_schema.dump(trans)
#       return jsonify(result)

@user.route("/cancel_loan/<id>",methods=["PUT"])
@flask_praetorian.auth_required
def cancel_loan(id):
    my_data = Loan.query.filter_by(id=id).first()
    my_data.status ="cancelled"
    db.session.commit()
    resp = jsonify("success")
    resp.status_code=200
    return resp


@user.route("/update_loan",methods=["PUT"])
@flask_praetorian.auth_required
def update_loan():
    my_data = Loan.query.filter_by(id=id).first()
    my_data.status = request.json["status"]
    db.session.commit()
    resp = jsonify("success")
    resp.status_code=200
    return resp


@user.route("/get_insurance",methods=["GET"])
@flask_praetorian.auth_required
def get_insurance():
     lst = Insurance.query.filter_by(created_by_id=flask_praetorian.current_user().id)
     result = insurance_schema.dump(lst)
     return jsonify(result)
     

@user.route("/add_insurance",methods=["POST"])
@flask_praetorian.auth_required
def add_insurance():
      insur = Insurance(
            name =request.json["name"],
      policy_number =request.json["policy_number"],
      email =request.json["email"],
      phone =request.json["phone"],
      address =request.json["address"],
      comments =request.json["comments"],
      
      status ="Pending",
      created_date = datetime.now().strftime('%Y-%m-%d %H:%M'),
      created_by_id = flask_praetorian.current_user().id
     
      )

      db.session.add(insur)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code=200
      return resp


@user.route("/cancel_insurance/<id>",methods=["PUT"])
@flask_praetorian.auth_required
def cancel_insurance(id):
     insur = Insurance.query.filter_by(id=id).first()
     insur.status ="cancelled"
     db.sesiion.commit()
     db.session.close()
     resp = jsonify("success")
     resp.status_code=200
     return resp


          
@user.route("/get_card",methods=["GET"])
@flask_praetorian.auth_required
def get_card():
      card = Card.query.filter_by(created_by_id=flask_praetorian.current_user().id).all()
     
      result = card_schema.dump(card)
      return jsonify(result)


@user.route("/get_my_card",methods=["GET"])
@flask_praetorian.auth_required
def get_my_card(): 
      user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
      card = Card.query.filter_by(name=user.firstname+' '+ user.lastname).all()
     
      result = card_schema.dump(card)
      return jsonify(result)
         

@user.route("/add_card",methods=["POST"])
@flask_praetorian.auth_required
def add_card():
     card = Card(
           
          name =request.json["name"],
          card_type =request.json["card_type"],
          card_number =request.json["card_number"],
          pin =request.json["pin"],    
     
          expiry_date =request.json["expiry_date"],
  

          status =request.json["status"],
          created_by_id = flask_praetorian.current_user().id,
          created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
     )

     db.session.add(card)
     db.session.commit()
     db.session.close()
     resp = jsonify("success")
     resp.status_code=200
     return resp


@user.route("/delete_card/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_card(id):
     card = Card.query.filter_by(id =id).first()
     db.session.delete(card)
     db.session.commit()
     db.session.close()
     resp = jsonify("success")
     resp.status_code=200
     return resp