from flask import Flask, render_template, redirect, session, flash
#from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

with app.app_context():
    connect_db(app)
    db.create_all()
#connect_db(app)
#app.app_context().push()
#db.create_all()
#toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """app homepage, redirect to register."""
    
    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register new user: produce form and handle form submission."""
    
    form = RegisterForm()
    if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
        
            new_user = User.register(username,password,email,first_name, last_name)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                form.username.errors.append('Username taken. Please pick another')
                return render_template('register.html', form=form)
            session['username'] = new_user.username
            flash('Welcome! Successfully Created Your Account!', "success")
                
            return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """produce login form and handle form submission"""
    form = LoginForm()
    if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            user = User.authenticate(username, password)
            if user:
                session['username'] = user.username
                flash(f"Welcome Back, {user.username}!", "primary")
                return redirect(f'/users/{user.username}')
            else:
                form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """Logout user."""
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/login')

@app.route('/users/<username>')
def show_user_info(username):
    """Show current logging in user info"""
    if "username" not in session or username != session['username']:
        #flash("Please login first!", "danger")
        #return redirect('/login')
        raise Unauthorized()
    
    #if "username" not in session:
    #    flash("Please login first!", "danger")
    #    return redirect('/login')
    
    user = User.query.get(username)
    form = DeleteForm()
    
    return render_template("users/show.html", user=user, form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def remove_user(username):
    """remove user and user's feedback from our DB and redirect to login page"""
    
    if "username" not in session or username != session['username']:
        #flash("Please login first!", "danger")
        #return redirect('/login')
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
        
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    """show add feedback form for logging in user & handle submission"""
    
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
        
            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            
            return redirect(f'/users/{new_feedback.username}')
    else:
        return render_template("feedback/add.html", form=form)
    
    
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """show update feedback form and handle form submission"""
    
    feedback = Feedback.query.get(feedback_id)
    
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    form = FeedbackForm(obj=feedback)
    
    if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            
            db.session.commit()
            
            return redirect(f'/users/{feedback.username}')
    else:
        return render_template("feedback/edit.html", form=form, feedback=feedback)
    
    
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """delete logging in user's feedback by owner."""
    
    feedback = Feedback.query.get(feedback_id)
    
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = DeleteForm()
    
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
            
    return redirect(f'/users/{feedback.username}')
