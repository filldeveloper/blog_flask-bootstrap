from flask import Flask, render_template, request
from post import Post
from datetime import datetime
import requests
import smtplib
import os

posts = requests.get('https://api.npoint.io/5deaf41b4f8078c817e6').json()
post_objects = []
for post in posts:
    post_obs = Post(
        post['id'], post['title'], post['subtitle'], post['body'], post['author'], post['date']
        )
    post_objects.append(post_obs)

date = datetime.now().year

OWN_EMAIL = os.environ.get('OWN_EMAIL')
OWN_PASSWORD = os.environ.get('OWN_PASSWORD')


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', posts=post_objects, date=date)


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in post_objects:
        if post.id == index:
            requested_post = post

    return render_template("post.html", post=requested_post, date=date)

@app.route('/about')
def about():
    return render_template('about.html', date=date)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html', date=date, msg_sent=False)
    else:
        data = request.form
        send_email(data["name"], data["email"], data["phonumber"], data["message"])
        return render_template('contact.html', date=date, msg_sent=True)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)

if __name__ == '__main__':
    app.run(debug=True)