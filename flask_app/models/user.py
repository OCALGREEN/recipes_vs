from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
from flask_app import app
from flask import flash
import re # imports compile to check email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # email format
bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod # CREATE 
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s,  %(email)s, %(password)s,NOW(), NOW());"
        result = connectToMySQL("recipes_schema").query_db(query, data)
        return result

    @classmethod # GET ID
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        print("QUERY IS: ", query)
        result = connectToMySQL("recipes_schema").query_db(query, data)
        return cls(result[0])
    
    @classmethod # GET EMAIL
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes_schema").query_db(query, data)
        print("RESULT", result)
        if len(result) < 1: # if the email entered is not in the database then return false
            return False
        return cls(result[0])

    @staticmethod # REGISTER VALIDATOR
    def register_validator(post_data):
        is_valid = True
        if not EMAIL_REGEX.match(post_data["email"]): # validate the email address
            flash("Please enter a valid email adress") # if the email does not match the email_regex format
            is_valid = False
        if len(post_data["first_name"]) < 2: # validates the first name
            flash("Please enter a valid first name")
            is_valid = False 
        if len(post_data["last_name"]) < 2: # validates the last name
            flash("Please enter a valid last name")
            is_valid = False 
        if len(post_data["password"]) < 6: # validates the password
            flash("Please enter a password longer than 6 characters")
            is_valid = False
        if post_data["password"] != post_data["confirm_password"]: # validates if both passwords entered match
            flash("Your password and confirm password do not match")
            is_valid = False
        return is_valid
    
    @staticmethod # LOGIN VALIDATOR
    def login_validator(post_data):
        is_valid = True
        user = User.get_by_email({"email": post_data["email"]}) # gets the email entered
        if not user: # checks to see if the email entered is good
            flash("Incorrect email")
            return False
        if not bcrypt.check_password_hash(user.password, post_data["password"]): # hashes the password entered and compares it to the hashed password in the database
            flash("Incorrect password")
            return False
        return is_valid