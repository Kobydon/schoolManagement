#================ wt forms ====#
from application.extensions.extensions import *
from application.settings.setup import app
# from application.database.user.user_db import Task,User


# from application.database.user.user_db import User

app.config['RECAPTCHA_PUBLIC_KEY']= '6LccceQaAAAAAFVTwhHp1SNNwddLxhpybkazgKYw'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LccceQaAAAAALRTre2F1LYBWHpykc9Fgv5ATkcd'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jxkalmhefacbuk@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Kwabena0541570527'
app.config['MAIL_PASSWORD'] = 'jymg qsic kais pebk'

 
 


ma = Marshmallow(app)
api =Api(app)
mail = Mail(app)
cors =CORS(app)




guard = flask_praetorian.Praetorian()
# db = SQLAlchemy(app)  

app.secret_key = 'secrete key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sms_db_mjof_user:YHCEcQho2AdSZHpjwHa2qSVmxwja1xA8@dpg-co23b0en7f5s73c9td9g-a.oregon-postgres.render.com/sms_db_mjof'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

app.config['SECRET_KEY'] = '0527'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 43}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}

# guard.init_app(app, User)
# login_manager = LoginManager()
# login_manager.init_app(app )
# login_manager.login_view = 'login'


