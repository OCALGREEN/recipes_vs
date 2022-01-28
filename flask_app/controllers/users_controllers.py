from flask import render_template, redirect, request, session 
from flask_app.models.user import User 
from flask_bcrypt import Bcrypt 
from flask_app import app
bcrypt = Bcrypt(app) 

@app.route("/")
def home():
    if "uuid" in session: # will send the user to the dashboard if they have signed in and not out yet
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not User.register_validator(request.form): # will check to see if all inputs are valid
        return redirect("/")
    else: # hashes the password and creates a new user
        hash_browns = bcrypt.generate_password_hash(request.form["password"]) # bcrypt function to hash the password
        user_data = {**request.form, "password": hash_browns} # stores the user input and the now hashed password in the varialbe
        session["uuid"] = User.create(user_data) # adds the user data to session to user late
        return redirect("/dashboard")

@app.route("/dashboard")
def success():
    if "uuid" not in session: # will send the user back to the home page if they are not logged in
        return redirect("/") 
    return render_template("dashboard.html", user = User.get_by_id({"id": session["uuid"]})) # renders dashboard and uses the id in session to grab user information

@app.route("/login", methods=["POST"])
def login():
    if not User.login_validator(request.form): # checks the email and password entered 
        return redirect("/")
    else: 
        user = User.get_by_email({"email": request.form["email"]}) # gets the user id and puts in the email
        session["uuid"] = user.id # puts the id in session
        return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear() # will clear session to prevent the user from entering without logging in
    return redirect("/")

@app.route("/create/new/recipe")
def create_new_recipe():
    return render_template("createnewrecipe.html")