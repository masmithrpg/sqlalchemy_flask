from . import app  

from flask_bootstrap import Bootstrap
from flask import Flask, request, render_template, url_for, redirect
from forms import RegistrationForm, LoginForm

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Bootstrap(app)
Base = declarative_base()

# engine = db.create_engine("ibmi://remotecmd:remote123@rgt", echo=True)
engine = sa.create_engine("ibmi://remotecmd:remote123@rgt")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
sa_session = Session()
# print(engine)
cnxn = engine.connect()
metadata = sa.MetaData()


class User(Base):
    __tablename__ = "USER"    
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(20), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    image_file = sa.Column(sa.String(20), nullable=False, default='default.jpg')
    password = sa.Column(sa.String(60), nullable=False)
    #posts = sa.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(Base):
    __tablename__ = "POST"    
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    date_posted = sa.Column(sa.DateTime, nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')" 


posts = [
	{'author': 'Corey Schafer',
    'title': 'blog Post 1',
    'content': 'First Post Content',
    'date_posted': 'October 7, 2021'
	},
	{'author': 'Mike Smith',
    'title': 'blog Post 2',
    'content': 'Second  Post Content',
    'date_posted': 'October 8, 2021'
	}
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)
    
@app.route('/about')
def about():
    return render_template('about.html', title = 'About')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for { form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been Logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)		

    
