#================ wt forms ====#
from application.extensions.extensions import *
from application.settings.setup import app
# from application.database.user.user_db import Task,User


# from application.database.user.user_db import User

app.config['RECAPTCHA_PUBLIC_KEY']= '6LccceQaAAAAAFVTwhHp1SNNwddLxhpybkazgKYw'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LccceQaAAAAALRTre2F1LYBWHpykc9Fgv5ATkcd'




 
 


ma = Marshmallow(app)
api =Api(app)

cors =CORS(app)




guard = flask_praetorian.Praetorian()
# db = SQLAlchemy(app)  

app.secret_key = 'secrete key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sus_fk82_user:ezIVJH1XIZP5YZ1P3plzY8Ph8Ptv31jB@dpg-co3jbnv79t8c738oknj0-a.oregon-postgres.render.com/sus_fk82'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'


app.config['SECRET_KEY'] = '0527'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 720}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}

# guard.init_app(app, User)
# login_manager = LoginManager()
# login_manager.init_app(app )
# login_manager.login_view = 'login'


