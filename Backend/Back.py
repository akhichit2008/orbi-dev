from flask_login import UserMixin,login_user,logout_user,login_required
from flask import Flask,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash as g,p
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ss'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db=SQLALCHRMY()
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'l'
login_manager.init_app(app)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(120))
db.create_all(app=app)
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
    user=User(email=email, name=name, password=g(password, method='sha256'))
    db.session.add(user)
    db.session.commit()
    return redirect("/l")
  return render_template("html")
@app.route("/l",methods=["POST","GET"])
def lo():
  if request.method=="POST":
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not p(user.password, password):
        flash('Please check your login details and try again.')
        return redirect("/l") 
    login_user(user)
    return redirect("/l")
  return render_template("html")
@app.route("/lo",methods=["GET"])
@login_required
def log():
  logout_user()
  return "logged out"
