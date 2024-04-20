from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.main_db.db import *
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
                "attitude","teacher_remark","interest","headmaster_remark","conduct",
                "attendance","class_term","grade","rank","pos","term","grade_id","staff_number","name",
                "status","amount","method","balance","paid_by","student","date","fees_type","cls",
                "other_name",
                "rme","science","math","social","pos","creativeart","careertech","english","computing",
                "ghanalanguage","student_name","all_total","school_name"
)
        
student_schema=StudentSchema(many=True)
student = Blueprint("student", __name__)
guard.init_app(app, User)
@student.route("/add_student",methods=['POST'])
@flask_praetorian.auth_required
def add_student():
      
      parent_name =request.json["parent_name"]
      firstname =request.json["first_name"]
      gender = request.json["gender"]
      lastname =request.json["last_name"]
      phone =request.json["phone"]
      email = request.json["email"]
      phone =request.json["phone"]
      address =request.json["address"]
      other_name =request.json["other_name"]
      student_name = firstname +" "+other_name+" "+lastname
      
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
      clname =request.json["class_name"]
      c_name = class_name[:5] 
      cls= Class.query.filter_by(class_name= class_name).first()
      cls.class_size = int(cls.class_size) + 1
    #   subject =request.json["subject"]
      created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
      created_by_id =flask_praetorian.current_user().id
     
      sch = School.query.filter_by(username=usr.username).first()
    
      sc = Student.query.filter_by(school_name=sch.school_name).count()
      cc = int(sc)+1
      first_three = sch.school_name[:4] + str(cc)
      student_number = first_three
    
     
      admitted_year =request.json["admitted_year"]
      picture_one =request.json["picture_one"]
    #   course_name =request.json[""]
      residential_status =request.json["resedential_status"]
      class_name =request.json["class_name"]
      if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
      elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:5] 
      else:
          c_name =class_name
      cls= Class.query.filter_by(class_name= class_name).first()
      cls.class_size = int(cls.class_size) + 1
    #   subject =request.json["subject"]
      created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
      created_by_id =flask_praetorian.current_user().id
      std = Student(other_name=other_name,created_by_id=created_by_id,picture=picture_one,class_name=clname ,created_date=created_date,parent_name=parent_name,school_name=school_name,
           student_number=student_number, admitted_year=admitted_year ,
           residential_status=residential_status,gender=gender,
           address=address,first_name=firstname,last_name=lastname,email=email,parent_phone =phone
           )
    #   bd =BroadSheet(student_name =student_name,class_name=class_name,student_number=student_number)
      bd =BroadSheet(student_name =student_name,class_name=c_name,student_number=student_number,
                     school_name =usr.school_name)
      usr = User(firstname=firstname,lastname=lastname,roles="student", username= student_number,
                   hashed_password= guard.hash_password(student_number),email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                                    school_name=school_name)
      db.session.merge(std)
      db.session.merge(bd)
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
    
     try:
          firstname =request.json["First Name"]
          
    
     except:
            firstname = ""
            
     try:
          other_name =request.json["Other Name"]
          
    
     except:
            other_name = ""
            
     try:
          last_name =request.json["Last Name"]
          
    
     except:
            last_name =""
            
     try:
          class_name =request.json["Class"]
          
    
     except:
            class_name =""
            
     try:
            gender = request.json["Gender"]
          
    
     except:
            gender =""
            
     try:
            dob = request.json["DoB"]
          
    
     except:
            dob =""
     
     try:
             phone =request.json["Phone"]
          
    
     except:
             phone = ""
     
     try:
             email =request.json["Email"]
          
    
     except:
            email =""
     try:
           address =request.json["Address"]
          
    
     except:
            address =""
            
 
     try:
           admitted_year =request.json["Admitted Year"]
          
    
     except:
            admitted_year =""
            
            
    
     try:
           admitted_year =request.json["Admitted Year"]
          
    
     except:
            admitted_year =""
            
     
     try:
           picture_one =request.json["picture_one"]
          
    
     except:
            picture_one =""
            
        
     try:
           residential_status =request.json["Resident"]
          
    
     except:
            residential_status =""
        
    #  try:
    #        residential_status =request.json["Resident"]
          
    
    # except:
    #         residential_status =""
     if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
     elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:5] 
                    
     else:
         c_name =class_name
     usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
     school_name= usr.school_name
     sch = School.query.filter_by(username=usr.username).first()
     school_name = sch.school_name
    #   numlst = list(range(400))
    #   n = random.shuffle(numlst)
     sc = Student.query.filter_by(school_name=sch.school_name).count()
     cc = int(sc)+1
     first_three = sch.school_name[:4] + str(cc)
     student_number = first_three
     student_name = firstname +" "+other_name+" "+last_name
     
    #  
    #   
     
    #   course_name =request.json[""]
    #  
    #  class_name =request.json["Class"]
     cls= Class.query.filter_by(class_name= request.json["Class"]).first()
     cls.class_size =  int(cls.class_size) + 1
    #   subject =request.json["subject"]
     created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
     created_by_id =flask_praetorian.current_user().id
     std = Student(created_by_id=created_by_id,class_name=class_name ,created_date=created_date,school_name=school_name,
           student_number=student_number,gender=gender,residential_status=residential_status,
           picture=picture_one,admitted_year=admitted_year,address=address,email=email,parent_phone=phone,

          first_name=firstname,last_name=last_name,other_name=other_name,dob=dob
           )
     
     bd=BroadSheet(student_name =student_name,class_name=c_name,student_number=student_number,
                    school_name=usr.school_name)
     usr = User(firstname=firstname,lastname=last_name,roles="student", username= student_number,
                   hashed_password= guard.hash_password(student_number),created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                   school_name=usr.school_name)
                   
     db.session.merge(std)
     db.session.merge(bd)
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
    std = Student.query.filter_by(school_name = user.school_name,class_name=cls.class_name).all()
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
      user = User.query.filter_by(username=std.student_number).first()
      bd = Broadsheet.query.filter_by(student_number=std.student_number).first()
      db.session.delete(user)
      db.session.delete(bd)
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
          student_number = request.json["student_number"]
          # stf = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          st = Student.query.filter_by(student_number = student_number).first()
          print(st.first_name)
          # midterm_score  = request.json["midterm_score"]
          class_name = st.class_name
          name = st.first_name+" "+st.other_name+" "+st.last_name
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
                  name=name,   school_name=school_name ,exams_score=exams_score ,created_by_id=created_by_id,total= total ,student_number=student_number ,class_name=class_name )
          
          bd = BroadSheet.query.filter_by(student_number=student_number).first()
          if (subject_name=="Science"):
              bd.science = total
              
          if (subject_name=="English"):
              bd.english = total
              
          if (subject_name=="Mathematics"):
              bd.math = total
              
          if (subject_name=="Creative Arts"):
              bd.creativeart = total
              
          if (subject_name=="Social Studies"):
              bd.social = total
              
          if (subject_name=="Computing"):
              bd.computing = total
              
          if (subject_name=="French"):
              bd.math = french
              
          if (subject_name=="Ghanaian Language"):
              bd.ghanalanguage = total
              
                  
          if (subject_name=="Career Tech"):
              bd.careertech = total
          
          today = datetime.today()
          bd.year=  today.year
          
          db.session.add(grade)
   
          db.session.commit()
     
          if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
          elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:5] 
          else:
                c_name =class_name
          grd = Grading.query.filter(Grading.class_name==c_name , Grading.subject_name==subject_name)
          
          
          bd = BroadSheet.query.filter_by(student_number=student_number).first()
          if (subject_name=="Science"):
              bd.science = total
              
          if (subject_name=="English"):
              bd.english = total
              
          if (subject_name=="Mathematics"):
              bd.math = total
              
          if (subject_name=="Creative Arts"):
              bd.creativeart = total
              
          if (subject_name=="Social Studies"):
              bd.social = total
              
          if (subject_name=="Computing"):
              bd.computing = total
              
          if (subject_name=="French"):
              bd.math = french
              
          if (subject_name=="Ghanaian Language"):
              bd.ghanalanguage = total
              
                  
          if (subject_name=="Career Tech"):
              bd.careertech = total
          
          today = datetime.today()
          bd.year=  today.year
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
          st = Student.query.filter_by(student_number = request.json["student_number"]).first()
          cls = Class.query.filter_by(staff_number = user.username).first()
          # midterm_score  = request.json["midterm_score"]
          class_name = st.class_name
        
        
          try:
                 class_score =  request.json["class_score"]
      
          except:
                  class_score =  ""          
          try:
                 exams_score =  request.json["exams_score"]
      
    
          except:
                  exams_score =  ""
          
          # total = request.json["total"]
         
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
    # t = Student.query.filter_by(student_number=student_number).first()
    bd  = BroadSheet.query.filter_by(student_number=student_number).first()
    bd.all_total = all_total
    # t.all_total = all_total
    db.session.commit()
    # grd = Student.query.filter(Student.class_name==t.class_name )
    # brd =  BroadSheet.query.filter(BroadSheet.class_name==bd.class_name)
    brd =  BroadSheet.query.filter(BroadSheet.class_name==bd.class_name,BroadSheet.school_name==user.school_name)
    lst1= brd.order_by(desc(BroadSheet.all_total)).all()

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
          
@student.route("/get_grade_by_class",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_grade_by_class():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    cls_name=  Class.query.filter_by(staff_number=user.username).first()
    
    grade = Grading.query.filter_by(class_name= cls_name.class_name)
    old = grade.order_by(desc(Grading.subject_name))
    result = student_schema.dump(grade)
    return jsonify(result)
# @student.route("/get_grade_by_first",methods=["POST","GET"])
# @flask_praetorian.auth_required
# def get_grade_by_first():
#     user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
#     cls_name=  Class.query.filter_by(staff_number=user.username).first()
    
#     grade = Grading.query.filter_by(class_name= cls_name.class_name,id=1)
#     old = grade.order_by(desc(Grading.subject_name))
#     result = student_schema.dump(grade)
#     return jsonify(result)
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
          head_master_remark = request.json["head_master_remark"]
          class_name = clas.class_name
         
          created_date  = datetime.now().strftime('%Y-%m-%d %H:%M')
          school_name = user.school_name
          
          student_number =  request.json["student_number"]
         
          created_by_id  = flask_praetorian.current_user().id
          
          today = datetime.today()
          year=  today.year
          
          rmk = Remark(teacher_remark=teacher_remark,attitude=attitude,interest=interest,attendance=attendance,class_name=class_name,
                 created_date=created_date   ,school_name=school_name,head_master_remark=head_master_remark,
                 year=year,
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
@student.route("/add_general_remark",methods=['POST'])
@flask_praetorian.auth_required
def add_general_remark():
        user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        cl = Class.query.filter_by(staff_number= user.username).first()
        
        try:
            student_number =request.json["student_number"]
        except:
            student_number=""
            
        try:
                first_name =request.json["first_name"]
        except:
            first_name= ""
        
        try:
                last_name =request.json["last_name"]
        except:
            last_name= ""
           
        try:    
            attitude =request.json["attitude"]
        except:
            attitude=""
            
        try:
            
            conduct =request.json["conduct"]
        except:
            conduct =""
        try:
            interest =request.json["interest"]
        except:
             interest =""
        try:
            headmaster_remark=request.json["headmaster_remark"]
        
        except:
             headmaster_remark=""
        try:
            teacher_remark= request.json["teacher_remark"]
            
        except:
             teacher_remark= ""
        try:
             term=request.json["term"]
           
        except :
            term=""
        today = datetime.today()
        year=  today.year
        created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
        class_name = cl.class_name
        created_by_id =flask_praetorian.current_user().id
        
        
        my_obj = GeneralRemark(attitude=attitude,interest=interest,conduct=conduct,
                               teacher_remark=teacher_remark,headmaster_remark=headmaster_remark,
                               term=term,year=year,student_number=student_number,class_name=class_name,
                               created_by_id=created_by_id)
        db.session.add(my_obj)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code=200
        return resp
        
        
        
        
@student.route("/update_general_remark",methods=['PUT'])
@flask_praetorian.auth_required
def update_general_remark():
        # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        # cl = Class.query.filter_by(staff_number= user.username).first()
        my_date = GeneralRemark.query.filter_by(student_number =request.json["student_number"]).first()
        
        try:
            my_date.student_number =request.json["student_number"]
        except:
            my_date.student_number= my_date.student_number
        
        
           
        try:    
             my_date.attitude =request.json["attitude"]
        except:
             my_date.attitude= my_date.attitude
            
        try:
            
             my_date.conduct =request.json["conduct"]
        except:
            my_date.conduct= my_date.conduct
        try:
              my_date.interest =request.json["interest"]
        except:
               my_date.interest= my_date.interest
        try:
            my_date.headmaster_remark=request.json["headmaster_remark"]
        
        except:
              my_date.headmaster_remark= my_date.headmaster_remark
        try:
            my_date.teacher_remark= request.json["teacher_remark"]
            
        except:
             my_date.teacher_remark= my_date.teacher_remark
        try:
              my_date.term=request.json["term"]
           
        except :
            my_date.term = my_date.term
        today = datetime.today()
        year=  today.year
        created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
        class_name = cl.class_name
        created_by_id =flask_praetorian.current_user().id
        
        
        my_obj = GeneralRemark(attitude=attitude,interest=interest,conduct=conduct,first_name=first_name,
                               last_name=last_name,created_date=created_date,
                               teacher_remark=teacher_remark,headmaster_remark=headmaster_remark,
                               term=term,year=year,student_number=student_number,class_name=class_name,
                               created_by_id=created_by_id)
        
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code=201
        return resp
        
@student.route("/get_broadsheet",methods=['GET'])
@flask_praetorian.auth_required
def get_broadsheet():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    stf = Staff.query.filter_by(staff_number=user.username).first()
    clas = Class.query.filter_by(staff_number = stf.staff_number).first()
    c_name = clas.class_name[:5] 
  
    if clas:
        rmk = BroadSheet.query.filter_by(school_name=user.school_name
                                      ,class_name=c_name).all()
        result = student_schema.dump(rmk)
    return jsonify(result) 

@student.route("/get_general_remark",methods=['GET'])
@flask_praetorian.auth_required
def get_general_remark():
    rmk = GeneralRemark.query.filter_by(created_by_id =flask_praetorian.current_user().id)
    result = student_schema.dump(rmk)
    return jsonify(result)
@student.route("/delete_remark/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_remark(id):
     my_data = GeneralRemark.query.filter_by(id=id).first()
     db.session.delete(my_data)
     db.session.commit()
     resp = jsonify("success")
     resp.status_code=201
     return resp