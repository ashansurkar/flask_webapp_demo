from flask import *
from practice import app, db_session, engine 
from practice.models import User
from practice.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
title= 'Flask Demo'

@app.route('/')
def hello():
    return render_template('base.html')

@app.route('/home')
@login_required
def home():
    users = User.query.all()
    return render_template('home.html',title=title,users=users, current_user= current_user)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username= form.username.data,
                    email= form.email.data,
                    )
        user.set_password(form.password.data)
        db_session.add(user)
        db_session.commit()
        login_user(user)
        flash('Your account has been created','success')
        return redirect(url_for('home'))
    # return render_template('home.html',users=users, current_user= current_user)
    # print('to register')
    return render_template('register.html', title=title,form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            nextpage = request.args.get('next')
            return redirect(nextpage or url_for('home'))
        flash(f'Login unsuccessful', 'danger')
    return render_template('login.html', title=title,form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))