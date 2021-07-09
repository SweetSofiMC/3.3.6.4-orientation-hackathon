import os
import smtplib
from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(
    user=os.getenv('POSTGRES_USER'),
    passwd=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=5432,
    table=os.getenv('POSTGRES_DB'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", username=session['username'], url=os.getenv("URL"))


@app.route('/about')
def about():
    return render_template('about.html', title="MLH Fellow", username=session['username'], url=os.getenv("URL"))


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title="Portfolio", username=session['username'], url=os.getenv("URL"))


@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume", username=session['username'], url=os.getenv("URL"))


@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", username=session['username'], url=os.getenv("URL"))


@app.route('/health')
def health():
    return "Success", 200


@app.route('/register', methods=('GET', 'POST'))
def register():
    print(request.method)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None

        if username is None:
            error = 'You need to provide a username'
        elif password is None:
            error = 'You need to provide a password'
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = "Username " + username + " is already taken."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            return render_template('register.html', username=session['username'], response="You've been successfully "
                                                                                           "registered")
        else:
            return render_template('register.html', response=error)
    if session['username'] is not None:
        return redirect(url_for('index'))
    else:
        return render_template('register.html', username=session['username'])


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session["username"] = username
            return render_template('login.html', username=session['username'], response=f"Welcome {user.username}"), 200
        else:
            return render_template('login.html', response=error), 418
    if session['username'] is not None:
        return redirect(url_for('index'))
    else:
        return render_template('login.html', username=session['username'])


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    if request.method == 'POST':
        session['username'] = None
        return redirect(url_for('login'))
    return render_template('logout.html', username=session['username'])


@app.route('/send-email', methods=['GET', 'POST'])
def send_email():
    response = "Your message was sent successfully!"

    try:
        # HTTP POST Request args
        email_sender = request.form['email']
        name = request.form['name']
        subject = request.form['subject']
        message_content = request.form['message']

        # Data from env
        email_server = os.environ.get('MAIL_SERVER')
        email_server_port = os.environ.get('MAIL_SMPT_PORT')
        email_username = os.environ.get('MAIL_USERNAME')
        email_password = os.environ.get('MAIL_PASSWORD')
        email_recipent = os.environ.get('MAIL_RECIPENT')

        # Email Data
        msg = MIMEText("Name: " + name + "\nContact email: " + email_sender + "\nMessage: " + message_content)
        msg['Subject'] = subject
        msg['From'] = email_username
        msg['To'] = email_recipent

        server = smtplib.SMTP_SSL(email_server, email_server_port)
        server.login(email_username, email_password)
        server.sendmail(email_username, [email_recipent], msg.as_string())
        server.quit()
    except:
        response = "Sorry, there was an error."

    return render_template('contact.html', title="Contact", response=response, url=os.getenv("URL"))
