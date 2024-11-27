from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.main_db.db import *
from sqlalchemy import or_,and_ ,desc ,cast, Float ,func
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
                "status","amount","method","balance","paid_by","student","date","fees_type","cls","picture",
                "other_name","promotion_status","dob",
                "rme","science","math","social","pos","creativeart","careertech","english","computing",
                "ghanalanguage","student_name","all_total","school_name","french","original_class_name","sa","admission_number","history",
                "owop","fees_amount","received_by"
)
        
student_schema=StudentSchema(many=True)
student = Blueprint("student", __name__)
guard.init_app(app, User)
@student.route("/add_student", methods=['POST'])
@flask_praetorian.auth_required
def add_student():
    # Extract request data
    parent_name = request.json.get("parent_name")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    gender = request.json.get("gender")
    phone = request.json.get("phone")
    email = request.json.get("email", "")
    address = request.json.get("address")
    picture = request.json.get("picture_one", "")
    other_name = request.json.get("other_name", "")
    admitted_year = request.json.get("admitted_year")
    residential_status = request.json.get("residential_status")
    class_name = request.json.get("class_name")

    # Construct full student name
    student_name = f"{first_name} {other_name} {last_name}".strip()

    # Get current user and school information
    usr = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    school_name = usr.school_name
    sch = School.query.filter_by(username=usr.username).first()
    acd = Academic.query.filter_by(school_name=school_name, status="current").first()

    # Handle class name logic and class size update
    cls = Class.query.filter_by(class_name=class_name).first()
    cls.class_size = int(cls.class_size) + 1
    c_name = class_name[:5] if class_name.startswith("JHS 1") else class_name[:6] if class_name.startswith("JHS 2") else class_name

    # Generate student number and ensure uniqueness
    sc = Student.query.filter_by(school_name=school_name).order_by(Student.created_date.desc()).first()
    if sc:
        cc = int(sc.id) + 1
    else:
        cc = Student.query.filter_by(school_name=school_name).count() + 1

    # Ensure unique student_number
    student_number = f"{school_name[:2]}{cc}"
    while User.query.filter_by(username=student_number).first():
        cc += 1
        student_number = f"{school_name[:2]}{cc}"

    # Check if student already exists
    existing_student = Student.query.filter(
        Student.first_name.contains(first_name),
        Student.last_name.contains(last_name),
        Student.other_name.contains(other_name)
    ).first()

    if existing_student:
        return jsonify("Student already exists"), 200

    # Create new Student, BroadSheet, and User entries
    std = Student(
        first_name=first_name,
        last_name=last_name,
        other_name=other_name,
        parent_name=parent_name,
        gender=gender,
        address=address,
        email=email,
        parent_phone=phone,
        admitted_year=admitted_year,
        residential_status=residential_status,
        class_name=class_name,
        student_number=student_number,
        picture=picture,
        school_name=school_name,
        created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        created_by_id=usr.id
    )

    bd = BroadSheet(
        student_name=student_name,
        class_name=c_name,
        student_number=student_number,
        school_name=school_name,
        original_class_name=class_name,
        current_status="",
        all_total="0",
        promotion_status="",
        term=acd.term,
        year=acd.year
    )

    user_entry = User(
        firstname=first_name,
        lastname=last_name,
        roles="student",
        username=student_number,
        hashed_password=guard.hash_password(student_number),
        email=email,
        created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        school_name=school_name
    )

    # Add and commit to the database
    db.session.add(std)
    db.session.add(bd)
    db.session.add(user_entry)
    db.session.commit()

    return jsonify("success"), 200
@student.route("/add_student_b_excel", methods=['POST'])
@flask_praetorian.auth_required
def add_student_b_excel():
    # Extract JSON data from request
    json_data = request.json
    
    # Extract fields with fallbacks for missing keys
    firstname = json_data.get("First Name", "")
    other_name = json_data.get("Other Name", "")
    last_name = json_data.get("Last Name", "")
    class_name = json_data.get("Class", "")
    admission_number = json_data.get("Admission Number", "")
    gender = json_data.get("Gender", "")
    dob = json_data.get("DoB", "")
    parent_name = json_data.get("Parent", "")
    phone = json_data.get("Phone", "")
    email = json_data.get("Email", "")
    address = json_data.get("Address", "")
    admitted_year = json_data.get("Admitted Year", "")
    picture_one = json_data.get("picture_one", "")
    residential_status = json_data.get("Resident", "")
    original_class_name = json_data.get("Class", "")

    # Handle class name variations
    if class_name in ["JHS 1A", "JHS 1B"]:
        c_name = class_name[:5]
    elif class_name in ["JHS 2A", "JHS 2B", "JHS 3A", "JHS 3B", "JHS 3C"]:
        c_name = class_name[:5]
    else:
        c_name = class_name

    # Get current user and related school info
    usr = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    acd = Academic.query.filter_by(school_name=usr.school_name, status="current").first()
    school_name = usr.school_name
    sch = School.query.filter_by(username=usr.username).first()

    # Generate student number and ensure uniqueness
    sc = Student.query.filter_by(school_name=school_name).order_by(Student.created_date.desc()).first()
    
    if sc:
        cc = int(sc.id) + 1
    else:
        cc = Student.query.filter_by(school_name=school_name).count() + 1

    # Ensure student_number is unique with the while loop
    student_number = f"{school_name[:7]}{cc}"
    if school_name == "Bibiani Community KG / Primary 'A'":
        student_number = f"{school_name[:5]}{cc}"

    while User.query.filter_by(username=student_number).first():
        cc += 1
        student_number = f"{school_name[:7]}{cc}"

    # Construct full student name
    student_name = f"{firstname} {other_name} {last_name}".strip()

    # Check if student already exists
    check_std = Student.query.filter(
        (Student.first_name + " " + Student.other_name + " " + Student.last_name) == student_name
    ).first()

    if check_std:
        return jsonify("Record already exists"), 200

    # Create new Student, BroadSheet, and User entries
    std = Student(
        created_by_id=usr.id,
        admission_number=admission_number,
        class_name=class_name,
        created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        school_name=school_name,
        student_number=student_number,
        gender=gender,
        residential_status=residential_status,
        picture=picture_one,
        admitted_year=admitted_year,
        address=address,
        email=email,
        parent_phone=phone,
        first_name=firstname,
        last_name=last_name,
        other_name=other_name,
        dob=dob,
        parent_name=parent_name
    )

    bd = BroadSheet(
        student_name=student_name,
        class_name=c_name,
        student_number=student_number,
        current_status="",
        school_name=usr.school_name,
        original_class_name=original_class_name,
        all_total="0",
        promotion_status="",
        term=acd.term,
        year=acd.year,
        owop="", history="", english="", math="", science="", socialstudies="",
        ghanalanguage="", creativeart="", social="", rme="", careertech="", pos="",
        created_date="", computing="", french="", aggregate=""
    )

    usr = User(
        firstname=firstname,
        lastname=last_name,
        roles="student",
        username=student_number,
        hashed_password=guard.hash_password(student_number),
        created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        school_name=usr.school_name
    )

    # Add and commit to the database
    db.session.add(std)
    db.session.add(bd)
    db.session.add(usr)
    
    try:
        db.session.commit()
        db.session.close()
        return jsonify("success"), 200
    except:
        db.session.rollback()
        return jsonify("Failed to add record"), 500

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
    # stf = Staff.query.filter_by(staff_number=user.username).first()
    cls = Class.query.filter_by(staff_number = user.username).first()
    std = Student.query.filter_by(school_name = user.school_name,class_name=cls.class_name)
    la = std.order_by(desc(Student.first_name),desc(Student.student_number))
    result = student_schema.dump(la)
    return jsonify(result)

@student.route("/student_out",methods=["PUT"])
@flask_praetorian.auth_required
def student_out():
     id = request.json["id"]
     std = Student.query.filter_by(id=id).first()
     std.class_name="Graduate"
     bd = BroadSheet.query.filter_by(student_number=std.student_number).first()
     bd.class_name="Graduate"
     user = User.query.filter_by(username=std.student_number).first()
     user.is_active=False
     db.session.commit()
     db.session.close()
     resp = jsonify("success")
     resp.status_code =201
     return resp

@student.route("/get_student",methods=['GET'])
@flask_praetorian.auth_required
def get_student():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    # acd=Academic.query.filter_by(school_name=user.school_name).first()
    # if(int(acd.countdown)<0):
    #     user.is_active = False
    #     db.session.commit()
    std = Student.query.filter(Student.school_name == user.school_name,Student.class_name != "Graduate").order_by(Student.first_name.asc())
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
      try:
           first_name= request.json["first_name"]  + ""
      except:
             first_name= "" 

      try:
           other_name= request.json["other_name"]  + ""
      except:
             other_name= ""

      try:
           last_name= request.json["last_name"]
      except:
             last_name= ""


      first_name = first_name
      last_name =  last_name
      other_name = other_name
      
      stf_data = Student.query.filter_by(id=id).first()
      
      try:
           picture= request.json["picture_one"]
      except:
             picture= stf_data.picture
      stf_data.first_name =request.json["first_name"]
      class_name = request.json["class_name"]
      stf_data.last_name =request.json["last_name"]
      stf_data.email = request.json["email"]
      stf_data.parent_phone =request.json["phone"]
      stf_data.address =request.json["address"]
      stf_data.other_name =request.json["other_name"]
      stf_data.picture = picture
      
    #   user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    #   stf_data.sch = School.query.filter_by(username=user.username).first()
    #   n = random.randint(0,100)
    #   first_three = sch.school_name[sch:3] + str(n)
      
      stf_data.parent_name = request.json["parent_name"]
      stf_data.class_name =request.json["class_name"]
     
      
    #   course_name =request.json[""]
      stf_data.residential_status =request.json["resedential_status"]
      stf_data.admitted_year =request.json["admitted_year"]

      if (class_name =="JHS 1A" or class_name=="JHS 1B"):
            c_name = class_name[:5] 
            
      elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
            c_name = class_name[:5] 
      else:
        c_name =class_name
      try:  
        stf_data.year_joined =request.json["year_joined"]
      except:
           stf_data.year_joined=""
      bd  = BroadSheet.query.filter_by(student_number = stf_data.student_number).first()
      bd.name = last_name +other_name+first_name
      
      bd.class_name =class_name
      bd.original_class_name =c_name
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
@student.route("/delete_student/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_student(id):
    # Find the student by ID
    student = Student.query.filter_by(id=id).first()
    
    if not student:
        resp = jsonify({"error": "Student not found"})
        resp.status_code = 404
        return resp

    # Update class size
    cls = Class.query.filter_by(class_name=student.class_name).first()
    if cls:
        cls.class_size = max(0, int(cls.class_size) - 1)
    
    # Find and delete associated user and broadsheet records
    user = User.query.filter_by(username=student.student_number).first()
    broadsheet = BroadSheet.query.filter_by(student_number=student.student_number).first()
    
    if user:
        db.session.delete(user)
    if broadsheet:
        db.session.delete(broadsheet)
    
    # Delete student record
    db.session.delete(student)
    
    # Commit the changes
    db.session.commit()
    
    # Return success response
    resp = jsonify({"message": "success"})
    resp.status_code = 201
    return resp

    
@student.route("/change_grade",methods=['POST'])
@flask_praetorian.auth_required
def change_grade():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          subject_name=  request.json["subject_name"]
          student_number = request.json["student_number"]
          id = request.json["id"]
          stc = Student.query.filter_by(student_number=student_number).first()
        #   cls = Class.query.filter_by(staff_number = user.username).first()
          # midterm_score  = request.json["midterm_score"]
          class_name = stc.class_name
          class_score = request.json["class_score"]
          # total = request.json["total"]
          exams_score =  request.json["exams_score"]
          created_date  = datetime.now().strftime('%Y-%m-%d %H:%M')
          school_name = user.school_name
       
          term = request.json["term"]
          status = "Pending"
          staff_number = user.username
        
          grade_id =request.json["id"]
          created_by_id  = flask_praetorian.current_user().id
          new_e = float(exams_score)
          new_c = float(class_score)
          total = new_e + new_c
         
          
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
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    
    # Apply order_by before calling .all()
    std = Student.query.filter(
        Student.school_name == user.school_name,
        Student.class_name != "Graduate"
    ).order_by(
        desc(Student.first_name), desc(Student.student_number)
    ).all()
    
    result = student_schema.dump(std)
    return jsonify(result)

      
@student.route("/add_grade",methods=['POST'])
@flask_praetorian.auth_required
def add_grade():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          acd=Academic.query.filter_by(school_name=user.school_name,status="current").first()
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
          tl = float(class_score) + float(exams_score) 
          total = int(exams_score) + int(class_score)
          new_class_score = float(class_score)
          new_exams_score = float(exams_score)
          grade=0
          score ="A"
          if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):
            if (total in range(80,101)):
                remark  = "Highest"
                
                grade = "1"
                score =1

          
                
            if (total in range(70,80)):
                remark  = "Higher"
            
                grade = "2"
                score = 2
               
                            
            if (total in range(60,70)):
                
              
                    grade = "3"
                    remark  = "High"
                    score=3
              
                
            if (total in range(55,60)):
                
               
                    grade = "4"
                    remark  = "Higher Average"
                    score =4
             
                
            if (total in range(50,55)):
      
                    grade = "5"
                    remark  = " Average"
                    score =5


            if (total in range(45,50)):
      
                    grade = "6"
                    remark  = " Low Averge"
                    score =6
             



            if (total in range(40,45)):
      
                    grade = "7"
                    remark  = " Low "
                    score =7
             

            if (total in range(35,40)):
      
                    grade = "8"
                    remark  = " Lower "
                    score =8

            if (total in range(0,35)):
      
                    grade = "9"
                    remark  = " Lower "
                    score =9



          else:

                if (total in range(80,101)):
                    remark  = "Highly Proficient"
                    
                  
                    score =1
                    grade   = "HP"
            
                if (total in range(66,80)):
                        remark  = "Proficient"
                        
                        score =""
                        grade   = "P"
                    
                                
                if (total in range(50,66)):
                    
                    
                 
                        grade = "AP"
                        remark  = " Approaching Proficiency"
                        score=""
                    
                if (total in range(40,50)):
                    
                   
                        grade   = "D"
                        remark  = "Developing"
                        score=""


             
        
          if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
          elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:5] 
          else:
                c_name =class_name
         
        
     
          bd = db.session.query(BroadSheet).filter_by(student_number=student_number).first()
          grading = db.session.query(Grading).filter_by(student_number=student_number).all()
          total_marks =  db.session.query(func.sum(cast(Grading.total,Float))).filter(Grading.student_number==student_number).scalar()
          bd.all_total = round( total_marks,1)
          print(bd.all_total)
                  
          classe = Class.query.filter_by(class_name=class_name).first()
          if(int(classe.grade_together) > 0):
                    grd = Grading.query.filter_by(class_name= bd.class_name , subject_name=subject_name,school_name=user.school_name,term=term,year=acd.year)     
          else:
                grd = Grading.query.filter_by(original_class_name=class_name , subject_name=subject_name,school_name=user.school_name,term=term,year=acd.year)     
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
          user = User.query.filter_by(id=flask_praetorian.current_user().id).first()

          acd=Academic.query.filter_by(school_name=user.school_name,status="current").first()
          subject_name=  request.json["subject_name"]
          remark  = "GOOD"
          grade =0
          score =0
          b="2"
          # stf = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          s_num  = request.json["student_number"]
          try:
                st = db.session.query(Student).filter_by(student_number=s_num).first()
                name = st.last_name+" "+st.other_name+" "+st.first_name

          except:
               return jsonify("not found")
          try:
               
            bd = BroadSheet.query.filter_by(student_number=s_num,term=acd.term,year=acd.year).first()
                
        #   print(name)
          # midterm_score  = request.json["midterm_score"]
            class_name = bd.class_name
            original_class_name=bd.original_class_name
         
          
        

          except:
               
               return jsonify({"error": "Student or BroadSheet record not found"})
          
      
        
          try:
                 class_score =  request.json["class_core"]
      
          except:
                  class_score =  0         
          try:
                 exams_score =  request.json["exams_score"]
      
    
          except:
                  exams_score = 0
          
          # total = request.json["total"]
          if class_score is not None:
                new_class_score = float(class_score)
                class_score =  float(class_score)
          else:
                 new_class_score =0.0
                 class_score = 0.0
                 
          if exams_score is not None:
                new_exams_score = float(exams_score)
                exams_score = float(exams_score)
                
          else:
                 new_exams_score =0.0
                 exams_score =0.0
          
          created_date  = datetime.now().strftime('%Y-%m-%d %H:%M')
          school_name = user.school_name
          student_number = request.json["student_number"]
          term = request.json["term"]
        
          today = datetime.today()
          year=  today.year
          created_by_id  = flask_praetorian.current_user().id
          scheme = Scheme.query.filter_by(created_by_id=flask_praetorian.current_user().id).first()
          
        
          l=2
          tl = class_score + exams_score

          total = int(class_score) + int(exams_score) 
          if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):
            if (total in range(80,101)):
                remark  = "Highest"
                
                grade = "1"
                score =1

          
                
            if (total in range(70,80)):
                remark  = "Higher"
            
                grade = "2"
                score = 2
               
                            
            if (total in range(60,70)):
                
              
                    grade = "3"
                    remark  = "High"
                    score=3
              
                
            if (total in range(55,60)):
                
               
                    grade = "4"
                    remark  = "Higher Average"
                    score =4
             
                
            if (total in range(50,55)):
      
                    grade = "5"
                    remark  = " Average"
                    score =5


            if (total in range(45,50)):
      
                    grade = "6"
                    remark  = " Low Averge"
                    score =6
             



            if (total in range(40,45)):
      
                    grade = "7"
                    remark  = " Low "
                    score =7
             

            if (total in range(35,40)):
      
                    grade = "8"
                    remark  = " Lower "
                    score =8

            if (total in range(0,35)):
      
                    grade = "9"
                    remark  = " Lower "
                    score =9



          else:

                if (total in range(80,101)):
                    remark  = "Highly Proficient"
                    
                  
                    score =1
                    grade   = "HP"
            
                if (total in range(66,80)):
                        remark  = "Proficient"
                        
                        score =""
                        grade   = "P"
                    
                                
                if (total in range(50,66)):
                    
                    
                 
                        grade = "AP"
                        remark  = " Approaching Proficiency"
                        score=""
                    
                if (total in range(40,50)):
                    
                   
                        grade   = "D"
                        remark  = "Developing"
                        score=""


         

                
                    
                # if (total in range(0,40)):
                 
                #         grade   = "E"
                #         remark  = "Emerging"
                #         score=""
        #   if (total in range(50,55)):
              
        #       if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):
        #           grade = 6
        #           remark  = " AVERAGE"
        #       else:
        #         grade   = "D"
        #         remark  = " CREDIT"
          
              
        #   if (total in range(45,50)):
              
        #       if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):
        #           grade = 7
        #           remark  = " PASS"
        #       else:
        #         grade   = "D"
        #         remark  = " CREDIT"
   
              
        #   if (total in range(40,45)):
        #       remark  = "PASS"
        #       if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):
        #           grade = 8

        #       else:
        #            print("yes")
              
         
      
              
        #   if (total in range(0,40)):
        #       remark  = " FAIL"
        #       if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):
        #           grade = 9
        #       else:
        #             print(("yes"))


        #   if 35 <= total < 45:
        #         remark = "PASS"
        #         if any(x in class_name.lower() for x in ["basic 1", "basic 2", "basic 3", "basic 4", "basic 5", "basic 6","KG 1","KG 2","Nursery 1","Nursery 2"]):
        #             grade = "E"
             
        #   if 0<= total < 35 and any(x in class_name.lower() for x in ["basic 1", "basic 2", "basic 3", "basic 4", "basic 5", "basic 6","KG 1","KG 2","Nursery 1","Nursery 2"]):
        #             grade = "F"
        #             remark = "FAIL"

          grade = Grading(name=name, subject_name= subject_name,remark=remark,class_score=new_class_score,created_date=created_date,term=acd.term,year=acd.year,grade=grade,score=score,
                     school_name=school_name ,original_class_name=original_class_name,exams_score=new_exams_score ,created_by_id=created_by_id,total= tl ,student_number=student_number ,class_name=class_name )
            
        #   bd = BroadSheet.query.filter_by(student_number=student_number).first()  
          bd = db.session.query(BroadSheet).filter_by(student_number=student_number,term=acd.term,year=acd.year).first()        
          gdi = Grading.query.filter_by(student_number=student_number,subject_name=subject_name,term=acd.term,year=acd.year).first()
          if gdi:
              return jsonify("skip")
          
          if total =="":
              return jsonify("skip")
          
          else:
                db.session.add(grade)
        
                try:
    # Perform database operations
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()  # Rollback the transaction on error
                    raise e  #d
               
            
        #   bd = BroadSheet.query.filter_by(student_number=student_number,year= acd.year,term=acd.term).first()
          
          if (subject_name=="Numeracy"):
                bd.numeracy = tl

          if (subject_name=="Literacy"):
                bd.literacy = tl
                      
          if (subject_name=="Writing"):
                bd.numeracy = tl
                                 
          if (subject_name=="Science"):
                bd.science = tl
                
          if (subject_name=="English"):
                bd.english = tl
                
          if (subject_name=="Mathematics" or subject_name=="Math"):
                bd.math = tl
                
          if (subject_name=="RME"):
                bd.rme = tl
                
          if (subject_name=="Creative Arts" or subject_name=="Creative Arts & Design" or subject_name=="Creative Art" ):
                bd.creativeart = tl
                
          if (subject_name=="Social Studies" or subject_name=="Social" ):
                bd.social = tl
                
          if (subject_name=="Computing" or  subject_name=="ICT"):
                bd.computing = tl
                
          if (subject_name=="French" or subject_name=="FRENCH"):
                bd.french = tl
                
          if (subject_name=="History"):
                bd.history = tl
                
          if (subject_name=="OWOP" or subject_name=="O.W.O.P"):
                bd.owop = tl
                
                
          if (subject_name=="Ghanaian Language" or subject_name=="Asante Twi"  or subject_name=="Twi" or "GA-LANGUAGE"):
                bd.ghanalanguage = tl

                    
          if (subject_name=="Career Tech" or subject_name=="Career Technology" or subject_name=="Carer Tech"):
                bd.careertech = tl
            
     
      
         
          agre_score= Grading.query.filter_by(student_number=student_number,term=acd.term,year=acd.year).order_by(Grading.score.asc()).limit(6).all()
        #   best_three = agre_score[:6]
          try:
            bd = db.session.query(BroadSheet).filter_by(student_number=student_number,term=acd.term,year=acd.year).first()
            cnm= bd.class_name
          except:
                return jsonify("skip")
         
          if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):  
                aggregate = sum(int(student.score) for student in agre_score)
                bd.aggregate = aggregate
                
          total_marks = db.session.query(func.sum(cast(Grading.total,Float))).filter(Grading.student_number==student_number,Grading.term==acd.term,Grading.year==acd.year).scalar()
         
          bd.all_total = round( total_marks,1)
          
        #   print(bd.all_total)

          grd=""
          classe = Class.query.filter_by(class_name=bd.class_name).first()
          if (int(classe.grade_together) > 0):
                    grd = Grading.query.filter_by(class_name= bd.class_name , subject_name=subject_name,school_name=user.school_name,term=acd.term,year=acd.year)     
          else:
                grd = Grading.query.filter_by(original_class_name=bd.original_class_name , subject_name=subject_name,school_name=user.school_name,term=acd.term,year=acd.year)     
          
          lst= grd.order_by(desc(Grading.total)).all()
          for(rank,g) in enumerate(lst):
          
            g.rank = rank+1
            
         
            
         
          try:
    # Perform database operations
                db.session.commit()
                db.session.close()
          except Exception as e:
                    db.session.rollback()  # Rollback the transaction on error
                    raise e 
        
          resp = jsonify("Success")
          resp.status_code=200
          return  resp            
        
        
@student.route("/all_total",methods=["POST"])
@flask_praetorian.auth_required
def all_total():
        all_total = request.json["all_total"]
        # canpost = request.json["canpost"]
        # tot =int(all_total)
        user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        

  
  
 
        student_number = request.json["student_number"]
        subject_name=  request.json["subject_name"]
    # t = Student.query.filter_by(student_number=student_number).first()
    # bd  = BroadSheet.query.filter_by(student_number=student_number).first()
    
    
        
   
        acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
        term = acd.term
        today = datetime.today()
        year=  today.year
        brd=""
        # std = Student.query.filter_by(student_number=student_number).first()
        try:
            bd = BroadSheet.query.filter_by(student_number=student_number).first()
            c =bd.class_name
            classe = Class.query.filter_by(class_name=bd.original_class_name).first()
            if (int(classe.grade_together) > 0):
                     brd =  BroadSheet.query.filter_by(class_name=c,school_name=user.school_name, term =term,year=acd.year)
            else:
                brd =  BroadSheet.query.filter_by(original_class_name=bd.original_class_name,school_name=user.school_name, term =term,year=acd.year)
       
        except :
            jsonify("not found")
       
       
     
        if not brd =="":
            lst1= brd.order_by(cast(BroadSheet.all_total, Float).desc()).all()
      
            rank = 1
            for student in lst1:
                student.pos = rank
                rank += 1
        
    # Perform database operations
        db.session.commit()
        db.session.close()      
        resp = jsonify("Success")
        resp.status_code=200
        return  resp            
        
            
 
 
 
@student.route("/my_grade",methods=["POST","GET"])
@flask_praetorian.auth_required
def my_grade():
      user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      subject_name = request.json["subject_name"]
      class_name = request.json["class_name"]
      acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
      term = acd.term
      today = datetime.today()
      year=  today.year
      grade = Grading.query.filter_by(original_class_name=class_name,subject_name=subject_name,
                                      created_by_id= flask_praetorian.current_user().id,
                                      term=term,year=acd.year)
      la = grade.order_by(desc(Grading.total))
      result = student_schema.dump(la)
      return jsonify(result)
      
@student.route("/get_grade_by_student",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_grade_by_student():
      student_number = request.json["student_number"]
      grade = Grading.query.filter_by(student_number=student_number).all()
      result = student_schema.dump(grade)
      return jsonify(result)


  
@student.route("/get_all_grades",methods=["GET"])
@flask_praetorian.auth_required
def get_all_grades():
      # student_number = request.json["student_number"]
      user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
      grade = Grading.query.filter_by(school_name=user.school_name)
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
      return jsonify(result)
  
@student.route("/get_pending_grades",methods=["GET"])
@flask_praetorian.auth_required
def get_pending_grades():
      # student_number = request.json["student_number"]
      user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
      grade = PendingGrade.query.filter_by(school_name=user.school_name)
      result = student_schema.dump(grade)
      return jsonify(result)


@student.route("/get_grading", methods=["POST"])
@flask_praetorian.auth_required
def get_grading():
    term = request.json["term"]
    year = request.json["year"]
    staff_number = request.json["staff_number"]  # Ensure this is a string

    # Convert staff_number to an integer
    # try:
        
    #     staff_number = int(staff_number)
    # except ValueError:
    #     print(staff_number)
    #     return jsonify({"error": "Invalid staff_number format. Expected an integer."}), 400

    user = User.query.filter_by(username=staff_number).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    grading_query = db.session.query(
        Grading.subject_name,
        Grading.original_class_name,
        Grading.term,
        Grading.year
    ).filter(
        Grading.year == year,
        Grading.term == term,
        Grading.created_by_id == user.id
    ).group_by(
        Grading.subject_name,
        Grading.original_class_name,
        Grading.term,
        Grading.year
    ).all()

    result = [
        {
            "subject_name": grade.subject_name,
            "class_name": grade.original_class_name,
            "term": grade.term,
            "year": grade.year
        }
        for grade in grading_query
    ]

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

@student.route("/search_sub_date",methods=["POST"])
@flask_praetorian.auth_required
def search_sub_date():
    date = request.json["date"]
    print(date)
    pay = FeesPayment.query.filter(SubPayment.date.contains(date) )
    lst = pay.order_by(desc(SubPayment.date))
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


@student.route("/search_pay_class",methods=["POST"])
@flask_praetorian.auth_required
def search_pay_class():
    class_name = request.json["class_name"]
    # print(date)
    pay = FeesPayment.query.filter(FeesPayment.cls.contains(class_name) )
    lst = pay.order_by(desc(FeesPayment.date))
    result = student_schema.dump(lst)
    return jsonify(result)

    

@student.route("/search_my_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_my_dates():
    date = request.json["date"]
   
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    bd = BroadSheet.query.filter_by(student_number=user.username).first()
    pay = FeesPayment.query.filter(FeesPayment.student.contains(bd.student_name),FeesPayment.date.contains(date))
    lst = pay.order_by(desc(FeesPayment.date))
    result = student_schema.dump(lst)
    return jsonify(result)
      
@student.route("/update_grade",methods=['PUT'])
@flask_praetorian.auth_required
def update_grade():
          user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
          student_number = request.json["student_number"]
          subject_name=  request.json["subject_name"]
          remark  = "GOOD"
          id = request.json["id"]
          term= request.json["term"]
          year = request.json
          grade_id = request.json["grade_id"]
          # stf = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          cls = Class.query.filter_by(staff_number = user.username).first()
          # midterm_score  = request.json["midterm_score"]
          class_name = request.json["class_name"]
          tl = float(request.json["class_score"]) + float(request.json["exams_score"]) 
        #   total = int(exams_score) + int(class_score)9
        #   new_class_score = float(class_score)
        #   new_exams_score = float(exams_score)
          Grade = Grading.query.filter_by(id=grade_id).first()
          Grade.class_score = request.json["class_score"]
          # total = request.json["total"]
          Grade.exams_score =  request.json["exams_score"]
          
        
          Grade.student_number = request.json["student_number"]
          Grade.term = request.json["term"]
          Grade.total =tl
          Grade.change_request ="Success"
          p_grade = PendingGrade.query.filter_by(id =id).first()
          p_grade.status="Success"
          # today = datetime.today()
          # year=  today.year
          exam= request.json["exams_score"]
          classa = request.json["class_score"]
          e_score = float(exam)
          cscore = float(classa)
        
          total = int(e_score) + int(cscore)
          grade="A"
          score =0
          if any(x in class_name.lower() for x in["jhs","basic7","basic8","basic9"]):
            if (total in range(80,101)):
                Grade.remark  = "Highest"
                
                Grade.grade = "1"
                Grade.score =1

          
                
            if (total in range(70,80)):
                Grade.remark  = "Higher"
            
                Grade.grade = "2"
                Grade.score = 2
               
                            
            if (total in range(60,70)):
                
              
                    Grade.grade = "3"
                    Grade.remark  = "High"
                    Grade.score=3
              
                
            if (total in range(55,60)):
                
               
                    Grade.grade = "4"
                    Grade.remark  = "Higher Average"
                    Grade.score =4
             
                
            if (total in range(50,55)):
      
                    Grade.grade = "5"
                    Grade.remark  = " Average"
                    Grade.score =5


            if (total in range(45,50)):
      
                    Grade.grade = "6"
                    Grade.remark  = " Low Averge"
                    Grade.score =6
             



            if (total in range(40,45)):
      
                    Grade.grade = "7"
                    Grade.remark  = " Low "
                    Grade.score =7
             

            if (total in range(35,40)):
      
                    Grade.grade = "8"
                    Grade.remark  = " Lower "
                    Grade.score =8

            if (total in range(0,35)):
      
                    Grade.grade = "9"
                    Grade.remark  = " Lower "
                    Grade.score =9



          else:

                if (total in range(80,101)):
                    Grade.remark  = "Highly Proficient"
                    
                  
                    Grade.score =1
                    Grade.grade   = "HP"
            
                if (total in range(66,80)):
                        Grade.remark  = "Proficient"
                        
                        Grade.score =""
                        Grade.grade   = "P"
                    
                                
                if (total in range(50,66)):
                    
                    
                 
                        Grade.grade = "AP"
                        Grade.remark  = " Approaching Proficiency"
                        Grade.score=""
                    
                if (total in range(40,50)):
                    
                   
                        Grade.grade   = "D"
                        Grade.remark  = "Developing"
                        Grade.score=""

     
          db.session.commit()
          tem =Grade.term
          yr = Grade.year
          stn = Grade.student_number
          print(yr)
          print(tem)
          print(stn)
          bd = db.session.query(BroadSheet).filter_by(student_number=stn,year=yr,term=tem).first()
          print(bd.year)
          grading = db.session.query(Grading).filter_by(student_number=student_number).all()
          total_marks =  db.session.query(func.sum(cast(Grading.total,Float))).filter(Grading.student_number==stn,Grading.term==tem,Grading.year==yr).scalar()
          bd.all_total = round( total_marks,1)
          print(bd.all_total)
                  
          grd = Grading.query.filter(Grading.class_name==class_name , Grading.subject_name==subject_name,Grading.year==yr,Grading.term==acd.term)
          
         
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





@student.route("/get_grade",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_grade():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    # student_number = request.json["student_number"]
    class_name = request.json["class_name"]
    term = request.json["term"]
    year = request.json["year"]
    grade = Grading.query.filter_by( term=term , year=year,original_class_name=class_name,school_name=user.school_name)
    result = student_schema.dump(grade)
    return jsonify(result)


@student.route("/search_my_result",methods=["POST","GET"])
@flask_praetorian.auth_required
def search_my_result():
    
    student_number = request.json["student_number"]
    class_name = request.json["class_name"]
    term = request.json["term"]
    year = request.json["year"]
    grade = Grading.query.filter_by(student_number= student_number ,   term=term , year=year,
                                    created_by_id =flask_praetorian.current_user().id)
    result = student_schema.dump(grade)
    return jsonify(result)
  

  
@student.route("/get_grade_analysis",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_grade_analysis():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    stf = Staff.query.filter_by(staff_number=user.username).first()
   
    acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
    term = acd.term
    today = datetime.today()
    year=  today.year
    c_name=""
    grd = Grading.query.filter_by(term=term,year=str(year),school_name=user.school_name).all()
    if(stf.form_master=="yes"):
        cls= Class.query.filter_by(staff_number=stf.staff_number,school_name=user.school_name).first()
        
        grd = Grading.query.filter_by(original_class_name=cls.class_name,term=term,year=acd.year,school_name=user.school_name).all()
    
    
    else:
        # cls= Class.query.filter_by(class_name=stf.class_name).first()
        grd = Grading.query.filter_by(created_by_id=flask_praetorian.current_user().id,term=term,year=acd.year,school_name=user.school_name).all()
       
    result = student_schema.dump(grd)
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
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
    term = request.json["term"]
    today = datetime.today()
    year=  request.json["year"]
    rmk = GeneralRemark.query.filter_by(student_number = student_number,term=acd.term,year=acd.year)
    result = student_schema.dump(rmk)
    return jsonify(result)
 
@student.route("/get_my_details",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_my_details():
     
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    std = Student.query.filter_by(student_number=user.username).all()
   
    result = student_schema.dump(std)
    return jsonify(result)
 
 

@student.route("/search_exact_class",methods=['POST'])
@flask_praetorian.auth_required
def search_exact_class():
      user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
      class_name = request.json["class_name"]
      std = Student.query.filter_by(class_name=class_name,school_name=user.school_name).all()
      result =  student_schema.dump(std)
     
      return jsonify(result)  
  
@student.route("/get_student_by_number",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_student_by_number():
    student_number = request.json["student_number"]
    std = Student.query.filter_by(student_number = student_number)
    # la = rmk.order_by(Grading.total.asc()).all
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
    std = Student.query.filter_by(student_number=student).first()
    name = std.last_name +" "+ std.other_name+" "+ std.first_name
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    created_by_id = flask_praetorian.current_user().id
    last_payment = db.session.query(FeesPayment).filter_by(student_number=student).order_by(FeesPayment.created_date.desc()).first()

    balance = int(ftype.total_amount)- int(amount)
    if last_payment:
        bc =  balance - int(last_payment.balance)
    else:
         bc =  balance - 0
    pmt = FeesPayment(student=name ,student_number=student, method=method,fees_type=fees_type,date=date,created_date=created_date,
                      
                      amount=amount,created_by_id=created_by_id ,balance=bc,school_name=school_name,cls= cls,paid_by=paid_by,
                      fees_amount=ftype.total_amount,received_by=user.firstname +" "+user.lastname)
    db.session.add(pmt)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp

@student.route("/add_sub_payment",methods=['POST'])
@flask_praetorian.auth_required
def add_sub_payment():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # student= request.json["student"]
    amount =request.json["amount"]
    method= request.json["method"]
    fees_type ="Subscription"
    # ftype = FeesType.query.filter_by(fees_type=fees_type).first()
    date =datetime.now().strftime('%Y-%m-%d')
    # paid_by = request.json["paid_by"]
    # cls =request.json["class"]
    school_name = user.school_name
    status= "Pending"
    # std = Student.query.filter_by(student_number=student).first()
    # name = std.last_name +" "+ std.other_name+" "+ std.first_name
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    created_by_id = flask_praetorian.current_user().id
    # balance = int(ftype.total_amount)- int(amount)
    pmt = SubPayment(status=status , method=method,fees_type=fees_type,date=date,created_date=created_date,
                      amount=amount,created_by_id=created_by_id ,school_name=school_name)
    db.session.add(pmt)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@student.route("/get_sub_payment_list",methods=['GET'])
@flask_praetorian.auth_required
def get_sub_payment_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    pmt = SubPayment.query.filter_by(school_name=user.school_name).all()
    result = student_schema.dump(pmt)
    return jsonify(result)

@student.route('/get_all_sub_payment_list', methods=['GET'])
@flask_praetorian.auth_required
def get_all_sub_payment_list():
    # Query to get all SubPayments in descending order of date
    sub_payments = SubPayment.query.order_by(desc(SubPayment.date)).all()
    
    # Serialize the query result using the schema
    result = student_schema.dump(sub_payments)
    
    # Return JSON response
    return jsonify(result)



@student.route('/get_sub_id/<id>', methods=['GET'])
@flask_praetorian.auth_required
def get_sub_id(id):
    # Query to get all SubPayments in descending order of date
    sub_payments = SubPayment.query.filter_by(id=id).all()
    
    # Serialize the query result using the schema
    result = student_schema.dump(sub_payments)
    
    # Return JSON response
    return jsonify(result)

    
@student.route("/update_sub_payment",methods=['PUT'])
@flask_praetorian.auth_required
def update_sub_payment():
    id = request.json["id"] 
    pmt = SubPayment.query.filter_by(id=id).first()
    acd=Academic.query.filter_by(school_name=pmt.school_name,status="current").first()
    user = User.query.filter_by(school_name=pmt.school_name,roles="admin").first()
    acd.countdown="10"
    pmt.status="Success"
    user.is_active=True
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@student.route("/get_payment_list",methods=['GET'])
@flask_praetorian.auth_required
def get_payment_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    pmt = FeesPayment.query.filter_by(school_name=user.school_name).order_by(desc(FeesPayment.created_date))

    result = student_schema.dump(pmt)
    return jsonify(result)

@student.route("/get_my_payment",methods=['GET'])
@flask_praetorian.auth_required
def get_my_payment():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    bd = BroadSheet.query.filter_by(student_number=user.username).first()
    pmt = FeesPayment.query.filter(FeesPayment.student_number.contains(bd.student_number)).all()
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
      user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
      class_name = request.json["class_name"]
    
      std = Student.query.filter_by(class_name=class_name,school_name=user.school_name)
      result = student_schema.dump(std)
      return jsonify(result)
@student.route("/add_general_remark",methods=['POST'])
@flask_praetorian.auth_required
def add_general_remark():
        user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        cl = Class.query.filter_by(staff_number= user.username).first()
        acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
        
        try:
            student_number =request.json["student_number"]
        except:
            student_number=""
            
        try:
                name =request.json["Name"]
        except:
            first_name= ""
        
        try:
                last_name =request.json["last_name"]
        except:
            last_name= ""
           
        try:
            attendance = request.json["Attendace(0 OUT OF total attendance)"]
        except:
            attendance=""
           
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
        # acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
        term = acd.term
        today = datetime.today()
        year=  acd.year
        created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
        class_name = cl.class_name
        created_by_id =flask_praetorian.current_user().id
        
        gdi = GeneralRemark.query.filter_by(student_number=student_number,year=year,term=term).first()
        if gdi:
            return jsonify("Skip")
        else:
            my_obj = GeneralRemark(attitude=attitude,interest=interest,conduct=conduct,attendance=attendance,
                                teacher_remark=teacher_remark,headmaster_remark=headmaster_remark,first_name=name,
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
        # class_name = cl.class_name
        created_by_id =flask_praetorian.current_user().id
        
        
        # my_obj = GeneralRemark(attitude=attitude,interest=interest,conduct=conduct,first_name=first_name,
        #                        last_name=last_name,created_date=created_date,
        #                        teacher_remark=teacher_remark,headmaster_remark=headmaster_remark,
        #                        term=term,year=year,student_number=student_number,class_name=class_name,
        #                        created_by_id=created_by_id)
        
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
    # if (clas.class_name =="JHS 1A" or clas.class_name=="JHS 1B"):
    #                 c_name = clas.class_name[:5] 
                    
    # elif (clas.class_name =="JHS 2A" or clas.class_name=="JHS 2B"):
    #                 c_name = clas.class_name[:5] 
  
    
    # else:
    #     c_name =clas.class_name
  
    acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
    rmk = BroadSheet.query.filter_by(school_name=user.school_name
                                      ,original_class_name=clas.class_name,term =acd.term ,year=acd.year)
    la = rmk.order_by(desc(BroadSheet.all_total))
    result = student_schema.dump(la)
    return jsonify(result) 




          
@student.route("/get_studentsheet",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_studentsheet():
    l="s"
    student_number = request.json["student_number"]
    class_name = request.json["class_name"]  
    term = request.json["term"]
    year = request.json["year"]
    if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
    elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:5] 
  
  
    elif (class_name =="JHS 3A" or class_name=="JHS 3B" or class_name=="JHS 3C"):
                    c_name = class_name[:5]     
    else:
        c_name =class_name
        
    bd = BroadSheet.query.filter_by(  term=term , year=str(year),student_number=student_number).all()    
    result = student_schema.dump(bd)
    return jsonify(result)

@student.route("/search_broadsheet",methods=["POST","GET"])
@flask_praetorian.auth_required
def search_broadsheet():
    
    user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
    class_name = request.json["class_name"]
    term = request.json["term"]
    year = request.json["year"]
    # if (class_name =="JHS 1A" or class_name=="JHS 1B"):
    #                 c_name = class_name[:5] 
                    
    # elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
    #                 c_name = class_name[:5] 
  
    
    # else:
    #     c_name =class_name
        
    bd = BroadSheet.query.filter_by(original_class_name= class_name ,   term=term , year=year,school_name=user.school_name)
    la = bd.order_by(desc(BroadSheet.all_total))
    result = student_schema.dump(la)
    return jsonify(result)
          
@student.route("/get_search_broadsheet_class",methods=["POST","GET"])
@flask_praetorian.auth_required
def get_search_broadsheet_class():
    
    user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
    class_name = request.json["promotion_class"]
    # term = request.json["term"]
    # year = request.json["year"]
    # if (class_name =="JHS 1A" or class_name=="JHS 1B"):
    #                 c_name = class_name[:5] 
                    
    # elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
    #                 c_name = class_name[:5] 
  
    
    # else:
    #     c_name =class_name
        
    bd = BroadSheet.query.filter(BroadSheet.original_class_name== class_name ,BroadSheet.school_name==user.school_name,
                                 BroadSheet.current_status.in_(['new',""]))
    la = bd.order_by(desc(BroadSheet.all_total))
    result = student_schema.dump(la)
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
 
 
@student.route("/delete_grading", methods=['POST', 'DELETE'])
@flask_praetorian.auth_required
def delete_grading():
    data = request.json  # Handle JSON data
    subject_name = data.get("subject_name")
    class_name = data.get("class_name")
    year = data.get("year")
    term = data.get("term")
    
    # Retrieve all matching grading entries
    grading_entries = Grading.query.filter_by(
        subject_name=subject_name,
        original_class_name=class_name,
        year=year,
        term=term
    ).all()

    if not grading_entries:
        return jsonify({"error": "Grading entries not found"}), 404

    # Retrieve all matching BroadSheet entries
    broadsheets = BroadSheet.query.filter_by(
        original_class_name=class_name,
        term=term,
        year=year
    ).all()

    # Update each matching BroadSheet entry
    for bd in broadsheets:
        setattr(bd, subject_name, "")  # Dynamically set attribute to an empty string

    # Delete all matching grading entries
    for entry in grading_entries:
        db.session.delete(entry)

    db.session.commit()
    return jsonify({"message": "Grading entries and BroadSheet entries updated successfully"}), 201


 
 
@student.route("/promote_student",methods=["POST","GET"])
@flask_praetorian.auth_required
def promote_student():
    
     user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
     class_name = request.json["promotion_class"]
     old_class = request.json["class_name"]
     student_number = request.json["student_number"]
     original_class_name =class_name
     year = request.json["year"]
     if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
     elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:5] 
                    
     elif (class_name =="JHS 3A" or class_name=="JHS 3B" or class_name=="JHS 3C"):
                    c_name = class_name[:5] 
     else:
         c_name =class_name
     bd = BroadSheet.query.filter_by(student_number=student_number,promotion_status= "Promoted").first()
     bc = BroadSheet.query.filter_by(student_number=student_number).first()
     std = Student.query.filter_by(student_number=student_number).first()
     old_data = BroadSheet.query.filter_by(student_number=student_number,original_class_name=old_class).first()
     if old_data:
         old_data.current_status ="old"
         old_data.promotion_status="Promoted"
     if std:
         std.class_name = class_name
     
     if bd:
         bd.class_name=c_name
         bd.original_class_name=class_name
        #  bd.year = year
         bd.promotion_status= "Promoted"
         db.session.commit()
         
     else:
        new =BroadSheet(student_name =bc.student_name,class_name=c_name,student_number=bc.student_number,promotion_status="Promoted",
                         all_total="0", current_status="new",  school_name =user.school_name,original_class_name=original_class_name)
        
        db.session.add(new)
        db.session.commit()
     resp = jsonify("success")
     resp.status_code=200
     return resp





 
@student.route("/repeat_student")
@flask_praetorian.auth_required
def repeat_student():
    
     user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
     class_name = request.json["promotion_class"]
     student_number = request.json["student_number"]
     original_class_name =class_name
     old_class = request.json["promotion_class"]
    #  year = request.json["year"]
     if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
     elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:5] 
                    
     elif (class_name =="JHS 3A" or class_name=="JHS 3B" or class_name=="JHS 3C"):
                    c_name = class_name[:5] 
     else:
         c_name =class_name
     bd = BroadSheet.query.filter_by(student_number=student_number,promotion_status="Repeated").first()
     bc = BroadSheet.query.filter_by(student_number=student_number).first()
     std = Student.query.filter_by(student_number=student_number).first()
     old_data = BroadSheet.query.filter_by(student_number=student_number,original_class_name=old_class).first()
     if old_data:
         old_data.current_status ="old"
         old_data.promotion_status="Repeated"
     if std:
         std.class_name = class_name
     
     if bd:
         bd.class_name=c_name
         bd.original_class_name=class_name
        #  bd.year = year
         bd.promotion_status= "Repeated"
         db.session.commit()
         
     else:
        new =BroadSheet(student_name =bc.student_name,class_name=c_name,student_number=bc.student_number,promotion_status="Repeated",
                        all_total="0",current_status="new",
                            school_name =user.school_name,original_class_name=original_class_name)
        db.session.add(new)
        db.session.commit()
    
     resp = jsonify("success")
     resp.status_code=200
     return resp



@student.route("/fix_error",methods=['POST'])
@flask_praetorian.auth_required
def fix_error():
      
      
      parent_name =request.json["parent_name"]
      firstname =request.json["first_name"]
      gender = request.json["gender"]
      lastname =request.json["last_name"]
      phone =request.json["phone"]
      email = request.json["email"]
      phone =request.json["phone"]
      address =request.json["address"]
      try:
        other_name =request.json["other_name"]
      except:
          other_name=""
      student_name = firstname +" "+other_name+" "+lastname
      
      usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      school_name= usr.school_name
      sch = School.query.filter_by(username=usr.username).first()
      acd=Academic.query.filter_by(school_name=usr.school_name,status="current").first()
    
      n = random.randint(0,100)
    #   first_three = sch.school_name[:4] + str(n)
    #   student_number = first_three
    
     
      admitted_year =request.json["admitted_year"]
    #   picture_one =request.json["picture_one"]
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
    
      sc = Student.query.filter_by(school_name=sch.school_name).order_by(Student.created_date.desc()).first()
      
      cc = int(sc.id)+1
     
      first_three = sch.school_name[:2] + str(cc)
      student_number = first_three
    
      try:
            admission_number = request.json["admission_number"]
            
      except:
            admission_number =""
      admitted_year =request.json["admitted_year"]
    #   picture_one =request.json["picture_one"]
    #   course_name =request.json[""]
      residential_status =request.json["resedential_status"]
      original_class_name =request.json["class_name"]
      class_name =request.json["class_name"]
      if (class_name =="JHS 1A" or class_name=="JHS 1B"):
                    c_name = class_name[:5] 
                    
      elif (class_name =="JHS 2A" or class_name=="JHS 2B"):
                    c_name = class_name[:6] 
      else:
          c_name =class_name
      cls= Class.query.filter_by(class_name= class_name).first()
      cls.class_size = int(cls.class_size) + 1
    #   subject =request.json["subject"]
      created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
      created_by_id =flask_praetorian.current_user().id
      find = Student.query.filter(Student.first_name.contains(firstname),Student.last_name.contains(lastname),
                                  Student.other_name.contains(other_name)).first()
      if find:
            resp = jsonify("success")
            resp.status_code =200
            return resp
      else:
            std = Student(other_name=other_name,created_by_id=created_by_id,class_name=clname ,created_date=created_date,parent_name=parent_name,school_name=school_name,
                student_number=student_number, admitted_year=admitted_year ,
                residential_status=residential_status,gender=gender,
                address=address,first_name=firstname,last_name=lastname,email=email,parent_phone =phone,admission_number=admission_number
                )
    #   bd =BroadSheet(student_name =student_name,class_name=class_name,student_number=student_number)
            bd =BroadSheet(student_name =student_name,class_name=c_name,student_number=student_number,current_status="",
                            school_name =usr.school_name,original_class_name=original_class_name,all_total="0",promotion_status="",term=acd.term,year=acd.year)
            usr = User(firstname=firstname,lastname=lastname,roles="student", username= student_number,
                        hashed_password= guard.hash_password(student_number),email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                                            school_name=school_name)
      db.session.add(std)
      db.session.add(bd)
      db.session.add(usr)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =200
      return resp