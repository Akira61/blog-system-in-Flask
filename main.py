from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# setup model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, title, content, timestamp):
        self.title = title
        self.content = content
        self.timestamp = timestamp


@app.route("/")
def index():
    return render_template("index.html", blogs= Post.query.all())

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        title = request.form["title"]
        post = request.form["post"]
        timestamp = datetime.now()
        new_post = Post(title=title, content=post, timestamp=timestamp)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("index"))
        
    return render_template("new.html")

@app.route("/post/<title>", methods= ["GET", "POST"])
def post(title):
    if request.method == "POST":     
        # update content
        new_title = request.form["title"]
        new_post = request.form["post"]
        new_timestamp = datetime.now()
        _post = Post.query.filter_by(title = title).first()
        _post.title = new_title
        _post.content = new_post
        _post.timestamp = new_timestamp
        db.session.commit()
        
        return redirect(url_for("index"))
    find_post = Post.query.filter_by(title = title).first()
    return render_template("post.html", title= find_post.title, post= find_post.content)

@app.route("/delete/<title>", methods=["POST"])
def delete(title):
    
    post = Post.query.filter_by(title=title).first()
    
    if post:
        Post.query.filter_by(title=title).delete()
        db.session.commit()
   
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)