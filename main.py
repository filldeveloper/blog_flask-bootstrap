from flask import Flask, render_template, request
from post import Post
from datetime import datetime
import requests
import json
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

print(OWN_EMAIL, OWN_PASSWORD)
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
    url = "https://be.trustifi.com/api/i/v1/email"

    payload = json.dumps({
    "recipients": [
        {
        "email": email,
        "name": name,
        "phone": {
            "country_code": "+55",
            "phone_number": phone
        }
        }
    ],
    "lists": [],
    "contacts": [],
    "attachments": [],
    "title": "Email enviado pelo blog",
    "html": message,
    "methods": {
        "postmark": False,
        "secureSend": False,
        "encryptContent": False,
        "secureReply": False
    }
    })
    headers = {
    'x-trustifi-key': os.environ.get('TRUSTIFI_KEY'),
    'x-trustifi-secret': os.environ.get('TRUSTIFI_SECRET'),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

if __name__ == '__main__':
    app.run(debug=True)