from flask import Flask, request, redirect, flash
from flask import render_template
from flask import current_app as app
from flask.helpers import url_for
from application.models import *
from flask_login import login_user, login_required, logout_user, current_user
from application.forms import RegistrationForm, LoginForm
from main import bcrypt
from application.database import db
from main import login_manager


@login_manager.user_loader
def load_user(id):
    print(User.query.get(int(id)))
    return User.query.get(int(id))


@app.route("/register", methods=["GET", "POST"])
def register():
    
    if current_user.is_authenticated:
        return redirect("/")
    form = RegistrationForm()
    
    if request.method=='POST':
        
        user = User(username=form.username.data)
        user.password=bcrypt.generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect("/login")
    
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
        user.active=1
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        
        return redirect("/")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    u = User.query.get(current_user.id)
    u.active=0
    db.session.commit()
    logout_user()
    return redirect(url_for('login')) 

@app.route('/')
@login_required
def index():
    
    u = User.query.get(current_user.id)
    
    decks = Deck.query.filter_by(user_id=u.id).all()
    
    return render_template('index.html', decks=decks)

@app.route('/deck/add', methods=['GET', 'POST'] )
def deck():
    u = User.query.get(current_user.id)
    if request.method=='POST':
        title = request.form['title']
        deck =Deck.query.filter((Deck.title==title) & (Deck.user_id==u.id)).first()
        if not deck:
            deck = Deck(title=title, user_id=u.id)
            db.session.add(deck)
            db.session.commit()
            return redirect('/')
        
            
    return render_template('deckadding.html')

@app.route('/deck/<int:deck_id>/delete')
def deck_delete(deck_id):
    deck = Deck.query.filter_by(id=deck_id).first()
    print(deck)
    if  deck:
        db.session.delete(deck)
        db.session.commit()
        return redirect('/')
    return redirect('/')

@app.route('/deck/<int:deck_id>/delete')
def deck_delete(deck_id):
    deck = Deck.query.filter_by(id=deck_id).first()
    if  deck:
        db.session.delete(deck)
        db.session.commit()
        return redirect('/')
    return redirect('/')

@app.route('/deck/<int:deck_id>/card/add',methods=['GET','POST'])
def card_add(deck_id):
    deck = Deck.query.filter_by(id=deck_id).first()
    if  deck:
        db.session.delete(deck)
        db.session.commit()
        return redirect('/')
    return redirect('/')













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


