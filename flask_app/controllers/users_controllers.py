from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("register.html")


@app.route("/validate_reg", methods=["POST"])
def register():
    if User.validate_reg(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash
        }
        user_id = User.register_user(data)
        session["user_id"] = user_id
        flash("User Created!")
        return redirect("/")
    else:
        return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    data = {
        "email":request.form["email"]
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email or Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Invalid Email or Password")
        return redirect("/")

    session["user_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    flash("You Have Logged Out")
    return redirect("/")


