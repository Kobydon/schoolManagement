from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.main_db.db import User,db,Student,School,Class,Staff,Grading,Scheme,Remark,PendingGrade,Payment,FeesType,FeesPayment

from sqlalchemy import or_,and_ ,desc
from datetime import datetime
from datetime import date
from flask import session
import random
class StudentSchema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","student_number","email","parent_name","admitted_year",
                "address","residential_status","parent_phone","address","phone","created_date",
                "form","class_name" ,"exams_score","midterm_score","class_score","total","remark","subject_name",
                "attitude","teacher_remark","interest","attendance","class_term","grade","rank","pos","term","grade_id","staff_number",
                "status","amount","method","balance","paid_by","student","date","fees_type","cls","other_name"
)
        









student_schema=StudentSchema(many=True)


student = Blueprint("student", __name__)
guard.init_app(app, User)





@student.route("/add_student",methods=['POST'])
@flask_praetorian.auth_required
def add_student():
      parent_name =request.json["parent_name"]
      firstname =request.json["first_name"]
      
      lastname =request.json["last_name"]
      phone =request.json["phone"]
      email = request.json["email"]
      phone =request.json["phone"]
      address =request.json["address"]
      other_name =request.json["other_name"]
      
      usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      school_name= usr.school_name
      sch = School.query.filter_by(username=usr.username).first()
    
      n = random.randint(0,100)
      first_three = sch.school_name[:4] + str(n)
      student_number = first_three
    
     
      admitted_year =request.json["admitted_year"]
      picture_one =request.json["picture_one"]

    #   course_name =request.json[""]
      residential_status =request.json["resedential_status"]
      class_name =request.json["class_name"]
      cls= Class.query.filter_by(class_name= class_name).first()
      cls.class_size = int(cls.class_size) + 1
    #   subject =request.json["subject"]
      created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
      created_by_id =flask_praetorian.current_user().id
      std = Student(other_name=other_name,created_by_id=created_by_id,picture=picture_one,class_name=class_name ,created_date=created_date,parent_name=parent_name,school_name=school_name,
           student_number=student_number, admitted_year=admitted_year ,
           residential_status=residential_status,
           address=address,first_name=firstname,last_name=lastname,email=email,parent_phone =phone
           )
    
      usr = User(firstname=firstname,lastname=lastname,roles="student", username= student_number,
                   hashed_password= guard.hash_password(student_number),email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                                    school_name=school_name)
      db.session.add(std)
      db.session.add(usr)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =200
      return resp





@student.route("/add_student_b_excel",methods=['POST'])
@flask_praetorian.auth_required
def add_student_b_excel():
    #   json_data = request.json
    #   for s in range(len(json_data)):
    #       if request.json["Resident" and "Branch" and "First Name" and "Address" and "Subject" and
    #                     "Email" and "Department" and "Phone" and "Bank" and "Account" and "Last Name" and 
    #                     "Joined"]:
              
    #   
      json_data = request.json
    #   parent_name =request.json["Parent"]
      firstname =request.json["First Name"]
      
      lastname =request.json["Last Name"]
    #   phone =request.json["Phone"]
    #   email = request.json["Email"]
    #   address =request.json["Address"]
      q = request.json["Other Name"]
      if q is not None and q != '':
           
             other_name =request.json["Other Name"]
        
      else: other_name =" "
      
      usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      school_name= usr.school_name
      sch = School.query.filter_by(username=usr.username).first()
      school_name = sch.school_name
      n = random.randint(0,100)
      first_three = sch.school_name[:4] + str(n)
      student_number = first_three
    
     
    #   admitted_year =request.json["Admitted Year"]
    #   picture_one =request.json["picture_one"]
     
    #   course_name =request.json[""]
    #   residential_status =request.json["Resident"]
      class_name =request.json["Class"]
      cls= Class.query.filter_by(class_name= class_name).first()
      cls.class_size = int(cls.class_size) + len(json_data)
    #   subject =request.json["subject"]
      created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
      created_by_id =flask_praetorian.current_user().id
      std = Student(created_by_id=created_by_id,class_name=class_name ,created_date=created_date,school_name=school_name,
           student_number=student_number,
           
          first_name=firstname,last_name=lastname,other_name=other_name
           )
    
      usr = User(firstname=firstname,lastname=lastname,roles="student", username= student_number,
                   hashed_password= guard.hash_password(student_number),email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                   school_name=school_name)
      db.session.add(std)
      db.session.add(usr)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =200
      return resp






@student.route("/get_class_by_student",methods=['GET'])
@flask_praetorian.auth_required
def get_class_by_student(): 
   
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    std = Student.query.filter_by(student_number=user.username).first()
    cls = Class.query.filter_by(class_name = std.class_name).first()
    std = Student.query.filter_by(school_name = user.school_name,class_name=cls.class_name)
    result = student_schema.dump(std)
    return jsonify(result)

@student.route("/get_student_by_class",methods=['GET'])
@flask_praetorian.auth_required
def get_student_by_class(): 
   
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    stf = Staff.query.filter_by(staff_number=user.username).first()
    cls = Class.query.filter_by(staff_number = stf.staff_number).first()
    std = Student.query.filter_by(school_name = user.school_name,class_name=cls.class_name)
    result = student_schema.dump(std)
    return jsonify(result)

@student.route("/get_student",methods=['GET'])
@flask_praetorian.auth_required
def get_student():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    std = Student.query.filter_by(school_name = user.school_name)
    result = student_schema.dump(std)
    return jsonify(result)



@student.route("/get_student_info/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_student_info(id):

    std = Student.query.filter_by(id=id)
    result = student_schema.dump(std)
    return jsonify(result)




@student.route("/update_student",methods=['PUT'])
@flask_praetorian.auth_required
def update_student():
    #   subject_name =request.json["subject_name"]
      id = request.json["id"]
      stf_data = Student.query.filter_by(id=id).first()
      stf_data.first_name =request.json["first_name"]
      
      stf_data.last_name =request.json["last_name"]
      stf_data.email = request.json["email"]
      stf_data.parent_phone =request.json["phone"]
      stf_data.address =request.json["address"]
      stf_data.other_name =request.json["other_name"]
     
    #   user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    #   stf_data.sch = School.query.filter_by(username=user.username).first()
    #   n = random.randint(0,100)
    #   first_three = sch.school_name[sch:3] + str(n)
      
      stf_data.parent_name = request.json["parent_name"]
      stf_data.class_name =request.json["class_name"]
     
      
    #   course_name =request.json[""]
      stf_data.residential_status =request.json["resedential_status"]
      stf_data.admitted_year =request.json["admitted_year"]
    #   stf_data.year_joined =request.json["year_joined"]
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp

@student.route("/delete_student/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_student(id):
      std = Student.query.filter_by(id=id).first()
      cls= Class.query.filter_by(class_name=std.class_name).first()
      cls.class_size = int(cls.class_size) - 1
      
      db.session.delete(std)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
    

@student.route("/change_grade",methods=['POST'])
@flask_praetorian.auth_required
def change_grade():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          subject_name=  request.json["subject_name"]
          id = request.json["id"]
          # stf = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          cls = Class.query.filter_by(staff_number = user.username).first()
          # midterm_score  = request.json["midterm_score"]
          class_name = cls.class_name
          class_score = request.json["class_score"]
          # total = request.json["total"]
          exams_score =  request.json["exams_score"]
          created_date  = datetime.now().strftime('%Y-%m-%d %H:%M')
          school_name = user.school_name
          student_number = request.json["student_number"]
          term = request.json["term"]
          status = "Pending"
          staff_number = user.username
        
          grade_id =request.json["id"]
          created_by_id  = flask_praetorian.current_user().id

          total = int(exams_score) + int(class_score)
         
          
          grade = PendingGrade( grade_id=grade_id,status=status,subject_name= subject_name,class_score=class_score,created_date=created_date,term=term,staff_number=staff_number,
                     school_name=school_name ,exams_score=exams_score ,created_by_id=created_by_id,total= total ,student_number=student_number ,class_name=class_name )
          db.session.add(grade)
          grd = Grading.query.filter_by(id=id).first()
          grd.change_request = "Pending"
   
          db.session.commit()
          
          resp = jsonify("success")
          resp.status_code=201
          return resp
        


@student.route("/get_all_students")
@flask_praetorian.auth_required
def get_all_students():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    std = Student.query.filter_by(school_name=user.school_name)
    result = student_schema.dump(std)
    return jsonify(result) 
  
      
@student.route("/add_grade",methods=['POST'])
@flask_praetorian.auth_required
def add_grade():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          subject_name=  request.json["subject_name"]
          remark  = "GOOD"
          # stf = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          cls = Class.query.filter_by(staff_number = user.username).first()
          # midterm_score  = request.json["midterm_score"]
          class_name = cls.class_name
         
          class_score = request.json["class_score"]
          # total = request.json["total"]
          exams_score =  request.json["exams_score"]
          created_date  = datetime.now().strftime('%Y-%m-%d %H:%M')
          school_name = user.school_name
          student_number = request.json["student_number"]
          term = request.json["term"]
        
          today = datetime.today()
          year=  today.year
          created_by_id  = flask_praetorian.current_user().id
          scheme = Scheme.query.filter_by(created_by_id=flask_praetorian.current_user().id).first()
          total = int(exams_score) + int(class_score)
          grade=0
          if (total in range(80,101)):
              remark  = "EXCELLENT"
              grade   = 1
              
              
          if (total in range(70,79)):
              remark  = "VERY GOOD"
              grade =2
              
                        
          if (total in range(60,69)):
              remark  = " GOOD"
              grade = 3
              
          if (total in range(55,59)):
              remark  = "CREDIT"
              grade = 4
          
              
          if (total in range(50,54)):
              remark  = " AVERAGE"
              grade = 5
          
              
          if (total in range(45,49)):
              remark  = " PASS"
              grade= 6
   
              
          if (total in range(40,44)):
              remark  = "  WEAK PASS"
              grade =7
              
              
          if (total in range(34,39)):
              remark  = " VERY WEAK PASS"
              grade = 8
              
          if (total in range(0,33)):
              remark  = " FAIL"
              grade = 9 
          
          grade = Grading( subject_name= subject_name,remark=remark,class_score=class_score,created_date=created_date,term=term,year=year,grade=grade,
                     school_name=school_name ,exams_score=exams_score ,created_by_id=created_by_id,total= total ,student_number=student_number ,class_name=class_name )
          db.session.add(grade)
   
          db.session.commit()
        


          grd = Grading.query.filter(Grading.class_name==class_name , Grading.subject_name==subject_name)
          
      
          lst= grd.order_by(desc(Grading.total)).all()
          for(rank,g) in enumerate(lst):
          
            g.rank = rank+1
            
         
            
          db.session.commit()
          db.session.close()
          resp = jsonify("Success")
          resp.status_code=200
          return  resp     
        
        
        
     
@student.route("/add_result_by_excel",methods=['POST'])
@flask_praetorian.auth_required
def add_result_by_excel():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          subject_name=  request.json["subject_name"]
          remark  = "GOOD"
          # stf = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          cls = Class.query.filter_by(staff_number = user.username).first()
          # midterm_score  = request.json["midterm_score"]
          class_name = cls.class_name
          class_score = request.json["class_score"]
          # total = request.json["total"]
          exams_score =  request.json["exams_score"]
          created_date  = datetime.now().strftime('%Y-%m-%d %H:%M')
          school_name = user.school_name
          student_number = request.json["student_number"]
          term = request.json["term"]
        
          today = datetime.today()
          year=  today.year
          created_by_id  = flask_praetorian.current_user().id
          scheme = Scheme.query.filter_by(created_by_id=flask_praetorian.current_user().id).first()
          total = int(exams_score) + int(class_score)
          grade=0
          if (total in range(80,101)):
              remark  = "EXCELLENT"
              grade   = 1
              
              
          if (total in range(70,79)):
              remark  = "VERY GOOD"
              grade =2
              
                        
          if (total in range(60,69)):
              remark  = " GOOD"
              grade = 3
              
          if (total in range(55,59)):
              remark  = "CREDIT"
              grade = 4
          
              
          if (total in range(50,54)):
              remark  = " AVERAGE"
              grade = 5
          
              
          if (total in range(45,49)):
              remark  = " PASS"
              grade= 6
   
              
          if (total in range(40,44)):
              remark  = "  WEAK PASS"
              grade =7
              
              
          if (total in range(34,39)):
              remark  = " VERY WEAK PASS"
              grade = 8
              
          if (total in range(0,33)):
              remark  = " FAIL"
              grade = 9 
          
          grade = Grading( subject_name= subject_name,remark=remark,class_score=class_score,created_date=created_date,term=term,year=year,grade=grade,
                     school_name=school_name ,exams_score=exams_score ,created_by_id=created_by_id,total= total ,student_number=student_number ,class_name=class_name )
          db.session.add(grade)
   
          db.session.commit()
        


          grd = Grading.query.filter(Grading.class_name==class_name , Grading.subject_name==subject_name)
          
      
          lst= grd.order_by(desc(Grading.total)).all()
          for(rank,g) in enumerate(lst):
          
            g.rank = rank+1
            
         
            
          db.session.commit()
          db.session.close()
          resp = jsonify("Success")
          resp.status_code=200
          return  resp            
        
        
@student.route("/all_total",methods=["POST","GET"])
@flask_praetorian.auth_required
def all_total():
    all_total = request.json["all_total"]
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()


   
    cls = Class.query.filter_by(staff_number = user.username).first()
    # midterm_score  = request.json["midterm_score"]
    # class_name = request.json["class_name"]
  
  
 
    student_number = request.json["student_number"]
    subject_name=  request.json["subject_name"]
    t = Student.query.filter_by(student_number=student_number).first()
    t.all_total = all_total
    db.session.commit()
    grd = Student.query.filter(Student.class_name==t.class_name )
    lst1= grd.order_by(desc(Student.all_total)).all()
    for(pos,g) in enumerate(lst1):
          
                  g.pos = pos+1
    db.session.commit()
    resp = jsonify("success")
    resp.status_code=200
    return resp
            
      
@student.route("/get_grade_by_student",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_grade_by_student():
      student_number = request.json["student_number"]
      grade = Grading.query.filter_by(student_number=student_number)
      result = student_schema.dump(grade)
      return jsonify(result)

@student.route("/get_pending_grades",methods=["GET"])
@flask_praetorian.auth_required
def get_pending_grades():
      # student_number = request.json["student_number"]
      user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
      grade = PendingGrade.query.filter_by(school_name=user.school_name)
      result = student_schema.dump(grade)
      return jsonify(result)
      
@student.route("/get_grade_id/<id>",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_grade_id(id):
      # student_number = request.json["student_number"]
      grade = Grading.query.filter_by(id=id)
      result = student_schema.dump(grade)
      return jsonify(result)
      
@student.route("/get_pending_grade_id/<id>",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_pending_grade_id(id):
      # student_number = request.json["student_number"]
      grade = PendingGrade.query.filter_by(id=id)
      result = student_schema.dump(grade)
      return jsonify(result)

@student.route("/searchdates",methods=["POST"])
@flask_praetorian.auth_required
def searchdates():
    date = request.json["date"]
    print(date)
    pay = PendingGrade.query.filter(PendingGrade.created_date.contains(date) )
    lst = pay.order_by(desc(PendingGrade.created_date))
    result = student_schema.dump(lst)
    return jsonify(result)

@student.route("/search_pay_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_pay_dates():
    date = request.json["date"]
    print(date)
    pay = FeesPayment.query.filter(FeesPayment.date.contains(date) )
    lst = pay.order_by(desc(FeesPayment.date))
    result = student_schema.dump(lst)
    return jsonify(result)
      
@student.route("/update_grade",methods=['PUT'])
@flask_praetorian.auth_required
def update_grade():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          subject_name=  request.json["subject_name"]
          remark  = "GOOD"
          id = request.json["id"]
          grade_id = request.json["grade_id"]
          # stf = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          cls = Class.query.filter_by(staff_number = user.username).first()
          # midterm_score  = request.json["midterm_score"]
          class_name = request.json["class_name"]
          Grade = Grading.query.filter_by(id=grade_id).first()
          Grade.class_score = request.json["class_score"]
          # total = request.json["total"]
          Grade.exams_score =  request.json["exams_score"]
          
        
          Grade.student_number = request.json["student_number"]
          Grade.term = request.json["term"]
          Grade.change_request ="Success"
          p_grade = PendingGrade.query.filter_by(id =id).first()
          p_grade.status="Success"
          # today = datetime.today()
          # year=  today.year
        
        
          total = int( request.json["exams_score"]) + int(request.json["class_score"])
          grade=0
          if (total in range(80,101)):
              Grade.remark  = "EXCELLENT"
              Grade.grade   = 1
              
              
          if (total in range(70,79)):
              Grade.remark  = "VERY GOOD"
              Grade.grade =2
              
                        
          if (total in range(60,69)):
              Grade.remark  = " GOOD"
              Grade.grade = 3
              
          if (total in range(55,59)):
              Grade.remark  = "CREDIT"
              Grade.grade = 4
          
              
          if (total in range(50,54)):
              Grade.remark  = " AVERAGE"
              Grade.grade = 5
          
              
          if (total in range(45,49)):
              Grade.remark  = " PASS"
              Grade.grade= 6
   
              
          if (total in range(40,44)):
              Grade.remark  = "  WEAK PASS"
              Grade.grade =7
              
              
          if (total in range(34,39)):
              Grade.remark  = " VERY WEAK PASS"
              Grade.grade = 8
              
          if (total in range(0,33)):
              Grade.remark  = " FAIL"
              Grade.grade = 9 
         
   
          db.session.commit()
        


          grd = Grading.query.filter(Grading.class_name==class_name , Grading.subject_name==subject_name)
          
      
          lst= grd.order_by(desc(Grading.total)).all()
          for(rank,g) in enumerate(lst):
          
            g.rank = rank+1
            
         
            
          db.session.commit()
          db.session.close()
          resp = jsonify("Success")
          resp.status_code=200
          return  resp     
        
          
@student.route("/search_result",methods=["POST","GET"])
@flask_praetorian.auth_required
def search_result():
    
    student_number = request.json["student_number"]
    class_name = request.json["class_name"]
    term = request.json["term"]
    year = request.json["year"]
    grade = Grading.query.filter_by(student_number= student_number ,   term=term , year=year)
    result = student_schema.dump(grade)
    return jsonify(result)


@student.route("/add_remark",methods=["POST"])
@flask_praetorian.auth_required
def add_remark():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          clas = Class.query.filter_by(staff_number=user.username).first()
          teacher_remark = request.json["teacher_remark"]
          attitude=  request.json["attitude"]
          interest  = request.json["interest"]
          attendance = request.json["attendance"]
          term = request.json["term"]
          class_name = clas.class_name
         
          created_date  = datetime.now().strftime('%Y-%m-%d %H:%M')
          school_name = user.school_name
          
          student_number =  request.json["student_number"]
         
          created_by_id  = flask_praetorian.current_user().id
          
          rmk = Remark(teacher_remark=teacher_remark,attitude=attitude,interest=interest,attendance=attendance,class_name=class_name,
                 created_date=created_date   ,school_name=school_name,
                 student_number=student_number ,created_by_id=created_by_id ,
                 class_term=term)
          
          db.session.add(rmk)
          db.session.commit()
          db.session.close()
          resp = jsonify("sucsess")
          resp.status_code=200
          return resp
        
        
 
@student.route("/get_student_remark",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_student_remark():
    student_number = request.json["student_number"]
    rmk = Remark.query.filter_by(student_number = student_number)
    result = student_schema.dump(rmk)
    return jsonify(result)
 
@student.route("/get_student_by_number",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_student_by_number():
    student_number = request.json["student_number"]
    std = Student.query.filter_by(student_number = student_number)
    result = student_schema.dump(std)
    return jsonify(result)





@student.route("/add_payment",methods=['POST'])
@flask_praetorian.auth_required
def add_payment():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    student= request.json["student"]
    amount =request.json["amount"]
    method= request.json["method"]
    fees_type =request.json["fees_type"]
    ftype = FeesType.query.filter_by(fees_type=fees_type).first()
    date =request.json["date"]
    paid_by = request.json["paid_by"]
    cls =request.json["class"]
    school_name = user.school_name
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    created_by_id = flask_praetorian.current_user().id
    balance = int(ftype.total_amount)- int(amount)
    pmt = FeesPayment(student=student , method=method,fees_type=fees_type,date=date,created_date=created_date,
 amount=amount,created_by_id=created_by_id ,balance=balance,school_name=school_name,cls= cls,paid_by=paid_by)

    db.session.add(pmt)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@student.route("/get_payment_list",methods=['GET'])
@flask_praetorian.auth_required
def get_payment_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    pmt = FeesPayment.query.filter_by(school_name=user.school_name).all()
    result = student_schema.dump(pmt)
    return jsonify(result)




@student.route("/get_payment/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_payment(id):

    subj = FeesPayment.query.filter_by(id=id)
    result = student_schema.dump(subj)
    return jsonify(result)




@student.route("/update_payment",methods=['PUT'])
@flask_praetorian.auth_required
def update_subject():
    id = request.json["id"]
    amount = request.json["amount"]
    sub_data = FeesPayment.query.filter_by(id=id).first()
    ftype = FeesType.query.filter_by(fees_type=sub_data.fees_type).first()
    sub_data.student = request.json["student"]
    sub_data.amount =request.json["amount"]
    sub_data.method = request.json["method"]
    sub_data.fees_type =request.json["fees_type"]
    sub_data.date =request.json["date"]
    sub_data.cls =request.json["class"]
    sub_data.paid_by =request.json["paid_by"]
    sub_data.balance = int(ftype.total_amount)- int(sub_data.amount) + int(amount)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@student.route("/delete_payment/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_payment(id):
      sub_data = FeesPayment.query.filter_by(id=id).first()
    
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp


@student.route("/search_house",methods=['POST'])
@flask_praetorian.auth_required
def search_house():
      class_name = request.json["class_name"]
    
      std = Student.query.filter_by(class_name=class_name)
      result = student_schema.dump(std)
      return jsonify(result)
