from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User

class Car:
    def __init__(self,data):
        self.id = data ['id']
        self.price = data ['price']
        self.model = data ['model']
        self.make = data ['make']
        self.year = data ['year']
        self.description = data ['description']
        self.user_id = data ['user_id']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']


    @classmethod
    def insert_car(cls,data):
        query="INSERT INTO cars (price,model,make,year,description,user_id) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(user_id)s)"  
        return connectToMySQL("dealership_project").query_db(query,data)


    @classmethod
    def get_cars(cls):
        query="SELECT * FROM users JOIN cars ON users.id = cars.user_id"
        results = connectToMySQL("dealership_project").query_db(query)
        users_cars = []

        for uc in results:
            user_instance = User(uc)
            car_data = {
                "id":uc["cars.id"],
                "price":uc["price"],
                "model":uc["model"],
                "make":uc["make"],
                "year":uc["year"],
                "description":uc["description"],
                "user_id":uc["user_id"],
                "created_at":uc["cars.created_at"],
                "updated_at":uc["cars.updated_at"]
            }
            user_instance.car = Car(car_data)
            users_cars.append(user_instance)
        
        return users_cars



    @classmethod
    def get_car(cls,data):
        query="SELECT * FROM users JOIN cars ON users.id = cars.user_id WHERE cars.id = %(car_id)s"
        results = connectToMySQL("dealership_project").query_db(query,data)
        user_instance = User(results[0])
        for uc in results:
            car_data = {
                "id":uc["cars.id"],
                "price":uc["price"],
                "model":uc["model"],
                "make":uc["make"],
                "year":uc["year"],
                "description":uc["description"],
                "user_id":uc["user_id"],
                "created_at":uc["cars.created_at"],
                "updated_at":uc["cars.updated_at"]
            }
            user_instance.car = Car(car_data)
        return user_instance



    @classmethod
    def edit_car(cls,data):
        query  = "SELECT * FROM cars WHERE id = %(car_id)s";
        result = connectToMySQL('dealership_project').query_db(query,data)
        return cls(result[0])


    @classmethod
    def update_car(cls,data):
        query = "UPDATE cars SET price=%(price)s,model=%(model)s,make=%(make)s,year=%(year)s,description=%(description)s WHERE id = %(car_id)s";
        return connectToMySQL("dealership_project").query_db(query,data)


    @classmethod
    def delete_car(cls,data):
        query="DELETE FROM cars WHERE id = %(id)s"  
        return connectToMySQL("dealership_project").query_db(query,data)




    @staticmethod
    def validate_car(car):
        is_valid = True
        if len(car["make"]) < 1:
            flash("Make is required")
            is_valid = False
        if len(car["model"]) < 1:
            flash("Model is required")
            is_valid = False
        if len(car["year"]) < 1:
            flash("Please enter valid year")
            is_valid = False
        if len(car["price"]) < 1:
            flash("Price must be greater than 0")
            is_valid = False
        if len(car["description"]) < 1:
            flash("Description is required")
            is_valid = False
        
        return is_valid


    @staticmethod
    def validate_update(car):
        is_valid = True
        if len(car["price"]) < 1:
            flash("Price must be greater than 0")
            is_valid = False
        if len(car["model"]) < 1:
            flash("Model is required")
            is_valid = False
        if len(car["make"]) < 1:
            flash("Make is required")
            is_valid = False
        if len(car["year"]) < 1:
            flash("Please enter valid year")
            is_valid = False
        if len(car["description"]) < 1:
            flash("Description is required")
            is_valid = False
        
        return is_valid
