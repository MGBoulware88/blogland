from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_toastr import Toastr
from flask_app.models import user, post
from datetime import datetime
bcrypt = Bcrypt(app)
toastr = Toastr(app)

###########################################
####### LANDING PAGE - NOT LOGGED IN ######
###########################################

####### REDIRECT TO HOME ROUTE #######
@app.route("/")
def go_home():
    return redirect("/home")


####### HOME ROUTE #######
@app.route("/home")
def home():
    return render_template("index.html")


###########################################
############## LOGIN AND REG ##############
###########################################

##### REG POST ROUTE #####
@app.route("/users/register", methods=['POST'])
def register():
    data = {
        **request.form
    }
    print(data)
    # validate form inputs
    if not user.User.validate_reg(request.form):
        return redirect("/errors")
    # if pass, hash pw then instantiate the user
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # override pw input with hashed pw
    data = {
        **request.form,
        'password':pw_hash
    }
    # store the id to pass into redirect
    user_id = user.User.create_user(data)
    session['user_data'] = user_id
    logged_user = user.User.read_one_user_by_id(user_id)
    return redirect("/users/dashboard")


###### REG FAIL REDIRECT #######
@app.route("/errors")
def reg_fail():
    return render_template("errors.html")

##### LOGIN POST ROUTE #####
@app.route("/users/login", methods=['POST'])
def login():
    #check email by trying to instantiate a user
    existing_user = user.User.read_one_user_by_email(request.form['email'])
    if not existing_user:
        flash("Invalid credentials", 'alert-danger')
        return redirect("/")
    #check pw
    if not bcrypt.check_password_hash(existing_user.password, request.form['password']):
        flash("Invalid credentials", 'alert-danger')
        return redirect("/")
    
    #if everything checks out, put the user's id into session
    session['user_id'] = existing_user.id
    return redirect("/users/dashboard")

####### LOGOUT #######
@app.route("/users/logout")
def logout():
    # clear session and return to home page
    session.clear()
    return redirect("/home")


##############################
####### USER DASHBOARD #######
##############################
@app.route("/users/dashboard")
def user_dashboard():
    # gatekeep all account pages - redirect to new page showing reg and login forms
    if 'user_id' not in session:
        return redirect("/users/unauthorized")

    #instantiate the logged in user
    logged_user = user.User.read_one_user_by_id(session['user_id'])

    #instantiate all posts w/ authors
    all_posts = post.Post.get_all_posts_and_authors()

    return render_template("dashboard.html", user=logged_user, posts=all_posts)

#####################################
####### UNAUTHORIZED REDIRECT #######
#####################################
@app.route("/users/unauthorized")
def unauthorized():
    return render_template("unauthorized.html") 

