from flask import Flask, request, redirect, flash
from flask import render_template
from flask import current_app as app
from flask.helpers import url_for
from application.models import *
from flask_login import login_user, login_required, logout_user, current_user
from application.forms import RegistrationForm, LoginForm
from main import bcrypt
from application.database import db



@app.route("/register", methods=["GET", "POST"])
def register():
    
    if current_user.is_authenticated:
        return redirect("/")
    form = RegistrationForm()
    print(1)
    if request.method=='POST':
        print('here')
        user = User(username=form.username.data, password=bcrypt.generate_password_hash(form.password.data))

        print(user.username, user.password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect("/login")
    print(2)
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    
    if request.method=='POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(user.password,form.password.data):
            flash('Invalid username or password')
            return redirect("/login")
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('feedback')) 

@app.route('/')

def index():

    return render_template('thank-you.html')


# @app.route("/articles_by/<user_name>", methods=["GET", "POST"])
# @login_required
# @roles_required("author")
# def articles_by_author(user_name):
#     articles = Article.query.filter(Article.authors.any(username=user_name))
#     return render_template(
#         "articles_by_author.html", articles=articles, username=user_name
#     )


# @app.route("/feedback", methods=["GET", "POST"])
# @login_required
# def feedback():
#     if request.method == "GET":
#         return render_template("feedback.html", error=None)
#     if request.method == "POST":
#         form = request.form
#         email = form["email"]
#         print(form)
#         # Validate here too
#         if "@" in email:
#             pass
#         else:
#             error = "Enter a valid email"
#             return render_template("feedback.html", error=error)

#         return render_template("thank-you.html")


# @app.route("/article_like/<article_id>", methods=["GET", "POST"])
# def like(article_id):
#     print("ARticle with article_id={}, was liked".format(article_id))

#     # Create a table fpr artic;e likes and store it.
#     return "OK", 200
