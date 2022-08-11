from flask_app import app
from flask import render_template,request,redirect,flash,session
from flask_app.models.car_model import Car
from flask_app.models.user_model import User



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in")
        return redirect("/")
    data = {
        "user_id":session["user_id"],
        "first_name":session["first_name"]
    }
    user = User.get_user(data)
    users_cars = Car.get_cars()
    return render_template("dashboard.html",user=user,users_cars=users_cars)


@app.route("/addcar")
def newcar():
    return render_template("add_car.html")

@app.route("/insertcar", methods=["POST"])
def insertcar():
    if "user_id" not in session:
        flash("Please log in")
        return redirect("/")

    if Car.validate_car(request.form):
        data = {
            "price":request.form["price"],
            "model":request.form["model"],
            "make":request.form["make"],
            "year":request.form["year"],
            "description":request.form["description"],
            "user_id":session["user_id"],
        }
        Car.insert_car(data)
        return redirect("/dashboard")
    else:
        return redirect("/addcar")


@app.route("/edit/<int:id>")
def edit_car(id):
    if "user_id" not in session:
        flash("Log in please")
        return redirect("/")
    data = {
        "car_id":id
    }
    return render_template("edit_car.html",user_car=Car.edit_car(data))


@app.route("/editcar",methods=["POST"])
def update_car():
    if "user_id" not in session:
        flash("Log in please")
        return redirect("/")

    if Car.validate_update(request.form):
        data = {
            "price":request.form["price"],
            "model":request.form["model"],
            "make":request.form["make"],
            "year":request.form["year"],
            "description":request.form["description"],
            "car_id":request.form["car_id"]
        }
        Car.update_car(data)
        session["price"] = request.form["price"]
        session["model"] = request.form["model"]
        session["make"] = request.form["make"]
        session["year"] = request.form["year"]
        session["description"] = request.form["description"]
        return redirect("/dashboard")
    else:
        return redirect(f"/edit/{request.form['car_id']}")



@app.route("/showcar/<int:id>")
def showcar(id):
    data = {
        "car_id":id
    }
    user_car = Car.get_car(data)
    return render_template("show_car.html",user_car=user_car)




@app.route("/delete/<int:id>")
def delete_car(id):
    if "user_id" not in session:
        flash("Log in please")
        return redirect("/")
    data = {
        "id":id
    }
    Car.delete_car(data)
    return redirect("/dashboard")