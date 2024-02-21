# from flask import Blueprint,render_template
# from flask.helpers import make_response
# from sqlalchemy.sql.functions import current_time
# #from application.database.user.user_db import Payment, Room_Type,Room, Task,db
# from  application.extensions.extensions import *
# from  application.settings.settings import *
# from  application.settings.setup import app
# # from application.forms import LoginForm
# from application.database import *
# from sqlalchemy import or_,desc,and_
# from datetime import datetime
# from datetime import date

# from datetime import datetime


# payment = Blueprint("payment", __name__)



# class taskSchema(ma.Schema):
#         class Meta:
#                 fields=("id","name")

# task_schema = taskSchema(many=True)

# class paymentSchema(ma.Schema):
#         class Meta:
#                 # Fields to ,,"category","post_on","price","image"
#                 fields = ("id","name","room","amount","discount","payment_date",
#                 "duration","floor","method","status","duration","checkout_date","check_date",
#                 "address")
   
# # room_schema = roomSchema()
# payments_schema = paymentSchema(many=True)
# payment_schema = paymentSchema()


# class roomTypeSchema(ma.Schema):
#         class Meta:
#                 # Fields to ,,"category","post_on","price","image"
#                 fields = ("id","room_type" )
   
# roomType_schema = roomTypeSchema()
# roomsType_schema = roomTypeSchema(many=True)


# @payment.route("/add_payment",methods=["POST"])
# @flask_praetorian.auth_required
# def add_payment():



#         amount =request.json["amount"]
#         name = request.json["name"]
#         floor = request.json["floor"]
    
#         room_type =request.json["room_type"]
#         duration = request.json["duration"]
#         method = request.json["method"]
      
    

#         payment_date = request.json["payment_date"]
#         discount = request.json["discount"]
#         check_in_date = request.json["check_in_date"]
#         check_out_date = request.json["check_out_date"]
#         adress = request.json["address"]
#         add_pay= Payment(name=name,amount=amount,duration=duration,floor=floor,
#         method=method,discount=discount,address=adress,room=room_type,payment_date=payment_date,check_date=check_in_date,
#         checkout_date=check_out_date,created_by_id= 
#         flask_praetorian.current_user().id,status="approved")
#         db.session.add(add_pay)
#         db.session.commit()
#         db.session.close()
#         resp = jsonify("sucess")
#         resp.status_code=201
#         return (resp)

  


# @payment.route("/get_payment",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def get_payment():
#         payments = db.session.query(Payment).all()
#         results = payments_schema.dump(payments)
#         return jsonify(results)


  

# @payment.route("/get_room",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def get_room():
#         room_lst = db.session.query(Room).all()
#         results =payments_schema.dump(room_lst)
        
#         return jsonify(results)



  
# @payment.route("/get_all_payment",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def get_all_payment():
#         payment_list = db.session.query(payment).all()
#         results =payments_schema.dump(payment_list)
        
#         return jsonify(results)

  
# @payment.route("/get_male_payment",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def get_male_payment():
#         payment_list = db.session.query(payment).filter_by(gender="male").all()
#         results =payments_schema.dump(payment_list)
        
#         return jsonify(results)

  
# @payment.route("/get_female_payment",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def get_female_payment():
#         payment_list = db.session.query(payment).filter_by(gender="female").all()
#         results =payments_schema.dump(payment_list)
        
#         return jsonify(results)


# @payment.route("/checkout_today",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def checkout_today():
#         current_time = datetime.now()
#         payment_list = db.session.query(payment).filter_by(checkout_date=current_time).all()
#         results =payments_schema.dump(payment_list)
        
#         return jsonify(results)




# @payment.route('/update_payment', methods=['PUT'])
# @flask_praetorian.auth_required
# def update_payment():
#          my_Data = payment.query.get(request.json.get('id'))
         
#          room_number = request.json["room_number"]
#         #  photo =request.json["photo"]
#          owner = Room.query.get(room_number)
#          my_Data.username= request.json["username"]
#          my_Data.room_number= room_number
#          my_Data.firstname = request.json["first_name"]
#          my_Data.lastname= request.json["last_name"]
#          my_Data.email= request.json["email"]
#          my_Data.password= request.json["password"]
#          my_Data.dob = request.json["dob"]
#          my_Data.country = request.json["country"]
#          my_Data.arrival_date = request.json["arrival_date"]
#         #  id_upload = request.json["id_upload"]
#         #  id_number =request.json["id_number"]
      
#          my_Data.id_type =request.json["id_type"]

      
#          my_Data.id_photo=  my_Data.id_photo
                
        
#          my_Data.id_number=my_Data.id_number
#          my_Data.checkout_date= request.json["checkout_date"]
#          my_Data.remark= request.json["remark"]
#          my_Data.work= request.json["work"]
#          my_Data.city = request.json["city"]
#          my_Data.gender = request.json["gender"]
#          my_Data.phone = request.json["phone"]
#          my_Data.address = request.json["address"]
#          my_Data.region = request.json["region"]
#         # room = request.json["room"]
      
     
        
#          owner.occupied_by = my_Data.firstname
#          owner.occupancy_state= "occupied"

#          db.session.commit()
       
#          resp = jsonify("sucess")
#          resp.status_code=201
#          return (resp)



# @payment.route("/get_payment_for/<id>")
# @flask_praetorian.auth_required
# def get_payment_for(id):
#     pay = db.session.query(Payment).filter_by(id=id).all()
#     results = payments_schema.dump(pay)
    
#     return jsonify(results)




# @payment.route('/delete_payment/<id>/',methods=['GET','DELETE'])
# @flask_praetorian.auth_required
# def delete_payment(id):
#      my_Data = payment.query.get(id)
#      db.session.delete(my_Data)
#      db.session.commit()
#      db.session.close()
#      resp =jsonify("deleted") 
    
#      return  (resp,201)

# @payment.route("/add_task",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def add_task():
#         name= request.json["task_name"]
#         add_task= Task(name=name,created_by_id=flask_praetorian.current_user().id)
#         db.session.add(add_task)
#         db.session.commit()
#         db.session.close()
      
#         resp = jsonify("sucess")
#         resp.status_code=201
#         return (resp)

  
 
# @payment.route("/get_task",methods=["GET","POST"])
# @flask_praetorian.auth_required
# def get_task():
#         task_lst = db.session.query(Task).all()
#         results =  task_schema.dump(task_lst)
        
#         return jsonify(results)



# # @payment.route("/update_house",methods=['PUT'])
# # @flask_praetorian.auth_required
# # def update_house():
# #      req = request.get_json()
# #      json_data = request.json
 
# # #
# #      for  s in range(len(json_data)):
        
# #         # if json_data[s]["task "]:
# #         #         task = json_data[s]["task"]

# #         if json_data[s]["status " and "occupancy_state" and "maintance_state" and "assignee" and "room_number"
# #         and "status" and "room_type" and "floor"and "reserved" and "task"]:
# #                 status =json_data[s]["status"]
       
# #                 occupancy_state = json_data[s]["occupancy_state"]

      
# #                 id_get = json_data[s]["id"] 

        
# #                 maintanace_state =json_data[s]["maintanace_state"]
       
# #                 assignee = json_data[s]["assignee"]


       
# #                 room_number = json_data[s]["room_number"]

# #         # if json_data[s]["room_type "]:
# #                 room_type = json_data[s]["room_type"] 
                
       
# #                 floor = json_data[s]["floor"]
   
# #                 #  Ads.query.get(request.json.get('id'))
# #                 owner = Room.query.get(id_get)
      
# #                 owner.picture_one= owner.picture_one
# #                 owner.picture_two= owner.picture_two
# #                 owner.picture_three= owner.picture_three
# #                 owner.maintance_state = maintanace_state
# #                 owner.room_type = room_type
# #                 owner.room_number=room_number
# #                 if json_data[s]["task"] == "":
# #                         owner.task = owner.task
# #                 else:
# #                         owner.task=json_data[s]["task"]
# #                 if json_data[s]["occupancy_state"] == "":
# #                         owner.occupancy_state = owner.occupancy_state
# #                 else:

# #                          owner.occupancy_state= json_data[s]["occupancy_state"]
# #                 if assignee == "":
# #                         owner.assignee = owner.assignee
# #                 else:
# #                         owner.assignee=  json_data[s]["assignee"]
# #                 owner.floor=floor
# #                 owner.room_type= room_type
# #                 owner.reserved =json_data[s]["reserved"]
# #                 owner.type="some"
# #                 owner.occupied_by = "kofi"
# #                 owner.duration=owner.duration
# #                 owner.session = owner.session
# #                 owner.create_by_id= flask_praetorian.current_user().id
                
# #                 if json_data[s]["status"] == "":
# #                         owner.status = owner.status
# #                 else:
# #                         owner.status = json_data[s]["status"]
                
             
       
# #                 db.session.commit()
                
# #                 # db.session.close()
# #                 print(owner.occupancy_state)
    
# #         #   resp.status_code =200  
                
# #                 resp = jsonify("success")
# #                 return(resp)




# # @payment.route("/get_payment/<id>")
# # @flask_praetorian.auth_required
# # def get_payment(id):
# #     payment = db.session.query(payment).filter_by(id=id).all()
# #     results = payments_schema.dump(payment)
    
# #     return jsonify(results)