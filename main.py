from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
from email_validator import validate_email,EmailNotValidError
import os
app = Flask(__name__)
load_dotenv()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail_username = os.environ.get("address_email")
mail_password = os.environ.get("password_email")
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.secret_key = os.environ.get("SECRET_KEY")
mail = Mail()
mail.init_app(app)

@app.route("/", methods=['POST', 'GET'])
@app.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    email_message=''
    if request.method=="POST":
        try:
            email = validate_email(request.form['email'], check_deliverability=False)
            valid_email = email.normalized
            print(f"-----------{valid_email}")
            greating_email = ''
            message = Message(subject='This is Your Crossword Solution',sender=mail_username ,recipients=[valid_email])
            message.html = greating_email
            mail.send(message)
            return '''<p style="color:#00ff4c;">Solution sent</p>'''
        except (ValueError,EmailNotValidError) as e:
            email_message=str(e)
        return f'''<p style="color:red;">{email_message}</p>'''
    print(f"================{email_message}")
    return render_template("index.html")


if __name__=='__main__':
    app.run(debug=True)