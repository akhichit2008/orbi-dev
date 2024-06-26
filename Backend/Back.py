from flask_login import UserMixin,login_user,logout_user,login_required,current_user
from flask import Flask,flash, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from main import call_agent
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ss'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.static_folder = 'static'
# sample href :- {{ url_for('static', filename='[css_folder]/[css-file].css') }}

db=SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'l'
login_manager.init_app(app)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(120))
class proj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100), unique=True)
    name=db.Column(db.String(100))
    des=db.Column(db.String(120))
with app.app_context():
    db.create_all()
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.route("/s",methods=["POST","GET"])
def si():
  if request.method=="POST":
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user: 
      return redirect("/l")
    user=User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(user)
    db.session.commit()
    return redirect("/l")
  return render_template("signup.html")

@app.route("/l",methods=["POST","GET"])
def lo():
  if request.method=="POST":
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect("/l") 
    login_user(user)
    return redirect("/l")
  return render_template("login.html")

@app.route("/lo",methods=["GET"])
@login_required
def log():
  logout_user()
  return "logged out"

@app.route("/p",methods=["GET"])
@login_required
def index(*b):
    return render_template("profile.html",current_user=current_user,project=proj.query.filter_by(email=current_user.email).first())

@app.route("/",methods=["GET"])
def index1(*b):
    return render_template("index.html")
@app.route("/sand",methods=["GET","POST"])
@login_required
def index(*b):
    if request.method=="POST":
        n1=request.form.get("n")
        call_agent(n)
    return render_template("sandbox.html")
if __name__ == "__main__":
  app.run()
