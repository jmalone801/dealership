from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re


class User:
    def __init__(self,data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']
        self.cars = []


    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("dealership_project").query_db(query,data)


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db =  connectToMySQL("dealership_project").query_db(query,data)

        if len(user_db) < 1:
            return False
        return cls(user_db[0])

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id=%(user_id)s"
        results = connectToMySQL("dealership_project").query_db(query,data)
        return cls(results[0])
        


    @staticmethod
    def validate_reg(user1):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        is_valid = True
        if len(user1["first_name"]) < 3:
            flash ("Must Enter First Name")
            is_valid = False

        if len(user1["last_name"]) < 3:
            flash ("Must Enter Last Name")
            is_valid = False

        if not email_regex.match(user1["email"]): 
            flash("Invalid Email Address")
            is_valid = False

        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = {
                    "email": request.form["email"]
                }
            result = connectToMySQL("dealership_project").query_db(query, data)
            if len(result) > 0:
                flash("Email Already Taken")
                is_valid = False

        if len(user1["password"]) < 8:
            flash ("Password Must Include At Least 8 Characters")
            is_valid = False

        if user1['confirm_password'] != user1['password']:
            flash("Passwords Must Match")
            is_valid = False

        return is_valid
