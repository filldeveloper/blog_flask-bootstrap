from flask import Flask, render_template
from post import Post
from datetime import datetime
import requests

posts = requests.get('https://api.npoint.io/5deaf41b4f8078c817e6').json()
post_objects = []
for post in posts:
    post_obs = Post(
        post['id'], post['title'], post['subtitle'], post['body'], post['author'], post['date']
        )
    post_objects.append(post_obs)

date = datetime.now().year
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

@app.route('/contact')
def contact():
    return render_template('contact.html', date=date)

if __name__ == '__main__':
    app.run(debug=True)