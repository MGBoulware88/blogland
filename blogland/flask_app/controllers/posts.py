from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import user, post
from datetime import datetime

####### SEARCH RESULTS DISPLAY ROUTE #######
@app.route("/search/results")
def show_search_results():
    return render_template("posts.html")


####### CREATE NEW POST DISPLAY ROUTE #######
# @app.route("/posts/create")
# def create_post():
#     return render_template("new_posts.html")

####### CREATE NEW POST POST ROUTE #######
@app.route("/posts/create", methods=['POST'])
def create_post():
    # save the post to the db
    post.Post.create_new_post(request.form)
    return redirect("/users/dashboard")

####### EDIT A POST POST ROUTE #######
@app.route("/posts/edit/<int:id>", methods=['POST'])
def edit_post(id):
    # generate the dict
    data = {
        **request.form,
        'id':id
    }
    # save the post to the db
    post.Post.edit_post_by_id(data)
    return redirect("/users/dashboard")


####### EDIT A POST POST ROUTE #######
@app.route("/posts/delete/<int:id>", methods=['POST'])
def delete_post(id):
    post.Post.delete_post_by_id(id)
    return redirect("/users/dashboard")


################################
######## SEARCH TESTING ########
################################
@app.route("/dynamic")
def dy_search():

    return render_template("search.html")