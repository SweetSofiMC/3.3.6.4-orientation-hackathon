import os
import smtplib
from flask import Flask, render_template, request
from dotenv import load_dotenv
from . import db
from app.db import get_db
from werkzeug.security import generate_password_hash
from email.mime.text import MIMEText

load_dotenv()
app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))


@app.route('/about')
def about():
    return render_template('about.html', title="MLH Fellow", url=os.getenv("URL"))


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title="Portfolio", url=os.getenv("URL"))


@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume", url=os.getenv("URL"))


@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", url=os.getenv("URL"))


@app.route('/health')
def health():
    return "Success", 200


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user = request.form['username']
        passwd = request.form['password']
        db = get_db()

        message = None
        error = False

        if not user:
            message = 'You need to provide a username'
            error = True
        elif not passwd:
            message = 'You need to provide a password'
            error = True
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (user,)
        ).fetchone() is not None:
            message = "Username "+user+" is already taken"
            error = True

        if not error:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (user, generate_password_hash(passwd))
            )
            db.commit()
            return "You've been successfully registered"
        else:
            return message, 400
    return "Register page apparently", 501




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
