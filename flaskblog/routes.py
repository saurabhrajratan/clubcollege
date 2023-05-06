import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


## Image uploading
# from flask import Flask, request, session, render_template, redirect
# from flask_sqlalchemy import SQLAlchemy
# from jinja2 import Template

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
# db = SQLAlchemy(app)

@app.route('/pyq')
def landingPage():
    olist = []
    for obj in Imagedetails.query.filter_by().all():
        olist.append(obj)
    if len(olist) == 0:
        return redirect('/get_details')
    else:
        return render_template("index.html", olist = olist)

@app.route('/get_details')
def getDetails():
    return render_template("get_details.html")

@app.route('/add_to_db', methods = ['GET', 'POST'])
def addToDb():
    if request.method == 'POST':
        iname = request.form.get('image_name')
        iurl = request.form.get('image_url')
        idesc = request.form.get('image_desc')
        idet = Imagedetails(iname = iname, iurl = iurl, idesc = idesc)
        db.session().add(idet)
        db.session().commit()
        id = Id(iid = idet.iid, iname = idet.iname)
        db.session().add(id)
        db.session.commit()
        return redirect("/pyq")
    return redirect("/pyq")   
@app.route('/print_details', methods = ['GET', 'POST'])
def printDetails():
    print(Id.query.filter_by().all())
    list = []
    for obj in Imagedetails.query.filter_by().all():
        list.append(obj)
    return render_template("print_details.html", list = list)
@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        retname = request.form.get('iname')
        ilist = [] #id list
        for obj in Id.query.filter_by().all():
            print(obj.iname)
            if obj.iname == retname:
                print(obj.iname)
                ilist.append(obj.iid)
        olist = [] # object list
        for id in ilist:
            # olist.append(Imagedetails.query.filter_by(iid = id))
            olist.append(Imagedetails.query.get(id))
        print(len(olist))
        if len(olist) == 0:
            return render_template('result_not_found.html')
        else:
            return render_template("show_searched_image.html", olist = olist)
    else:
        print("inside else body")
        print(request.method)
        return redirect("/pyq")
@app.route('/show/<int:iid>')
def show(iid):
    iobj = Imagedetails.query.get(iid)
    return render_template("show_idetails.html", iobj = iobj)
@app.route('/<int:iid>/edit', methods=['GET', 'POST'])
def edit(iid):
    if request.method == 'POST':
        iname = request.form.get('iname')
        idesc = request.form.get('idesc')
        iurl = request.form.get('iurl')
        ret_obj = Imagedetails.query.get(iid)
        ret_obj.iname = iname
        ret_obj.idesc = idesc
        ret_obj.iurl = iurl
        db.session().commit()
        ret_id_obj = Id.query.get(iid)
        ret_id_obj.iid = iid
        ret_id_obj.iname = iname
        print(ret_id_obj.iname)
        db.session().commit()
        print("inside if")
        return redirect('/pyq')
    iobj = Imagedetails.query.get(iid)
    return render_template("edit_idetails.html", iobj = iobj)
@app.route('/delete/<int:iid>')
def delete(iid):
    ret_obj = Imagedetails.query.get(iid)
    db.session.delete(ret_obj)
    db.session().commit()
    ret_id_obj = Id.query.get(iid)
    db.session.delete(ret_id_obj)
    db.session().commit()
    return redirect('/pyq')

class Imagedetails(db.Model):
    iid = db.Column(db.Integer, primary_key = True)
    iname = db.Column(db.String, nullable = False)
    iurl = db.Column(db.String, nullable = False)
    idesc = db.Column(db.String, nullable = False)
    ilist = db.relationship('Id', backref = 'imagedetails')

class Id(db.Model):
    iid = db.Column(db.Integer, primary_key = True)
    iname = db.Column(db.String)
    # id = db.Column(db.Integer, primary_key = True)
    piname = db.Column(db.String, db.ForeignKey("imagedetails.iname"))#parent image name

# if __name__ == '__main__':
#     @app.before_first_request
#     def create_tables():
#         db.create_all()
#     app.run(debug = True, port = 8080)