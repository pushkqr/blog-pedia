from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, EditProfileForm
import smtplib
import os
from models import User, BlogPost, Comment, Category, Tag, PostTag
from extensions import db, login_manager, ckeditor, bootstrap
from sqlalchemy.orm import DeclarativeBase
from flask_gravatar import Gravatar

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")

ckeditor.init_app(app)
bootstrap.init_app(app)
login_manager.init_app(app)
gravatar = Gravatar(app=app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///test.db")
db.model_class = Base
db.init_app(app)


def init_default_categories():
    default_categories = [
        "Technology",
        "Business",
        "Lifestyle",
        "Health & Fitness",
        "Travel",
        "Food & Cooking",
        "Arts & Culture",
        "Education",
        "Science",
        "Entertainment",
        "Sports",
        "Personal Development",
        "Books & Literature",
        "Career",
        "Gaming"
    ]

    for category_name in default_categories:
        existing = Category.query.filter_by(name=category_name).first()
        if not existing:
            new_category = Category(name=category_name)
            db.session.add(new_category)

    try:
        db.session.commit()
        print("Default categories created successfully!")
    except Exception as e:
        print(f"Error creating default categories: {e}")
        db.session.rollback()


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and int(current_user.get_id()) == 1:
            return func(*args, **kwargs)
        abort(403)

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_auth_status():
    admin = False
    if current_user.is_authenticated:
        admin = int(current_user.get_id()) == 1
    return {'logged_in': current_user.is_authenticated,
            'admin': admin}


with app.app_context():
    db.create_all()
    init_default_categories()


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.data.get('name')
        email = form.data.get('email')
        password = form.data.get('password')
        join_date = datetime.today()
        bio = f"Hey! I'm {name}"

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User Already Exists. Please Log In.")
            return redirect(url_for('login'))

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8),
            bio=bio,
            join_date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=form)


@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = BlogPost.query.filter_by(author_id=user_id).order_by(BlogPost.date.desc()).all()
    comments = Comment.query.filter_by(author_id=user_id).order_by(Comment.id.desc()).all()

    return render_template('profile.html',
                           user=user,
                           posts=posts,
                           comments=comments)


@app.route('/profile/edit', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.bio = form.bio.data

        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('user_profile', user_id=current_user.id))

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.bio.data = current_user.bio

    return render_template('edit-profile.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data.get('email')
        password = form.data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('get_all_posts'))
        else:
            flash("Invalid Email Address/Password.")
            return redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = BlogPost.query.filter_by(category_id=category_id).order_by(BlogPost.date.desc()).all()
    return render_template('index.html', all_posts=posts, title=f"Category: {category.name}")


@app.route('/tag/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = [post_tag.post for post_tag in tag.posts]
    return render_template('index.html', all_posts=posts, title=f"Tagged with: {tag.name}")


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if query:
        posts = BlogPost.query.filter(
            db.or_(
                BlogPost.title.ilike(f'%{query}%'),
                BlogPost.subtitle.ilike(f'%{query}%'),
                BlogPost.body.ilike(f'%{query}%'),
                BlogPost.tags.any(PostTag.tag.has(Tag.name.ilike(f'%{query}%'))),
                BlogPost.category.has(Category.name.ilike(f'%{query}%')),
                BlogPost.author.has(User.name.ilike(f'%{query}%'))
            )
        ).order_by(BlogPost.date.desc()).all()
    else:
        posts = []

    if posts:
        results_count = {
            'total': len(posts),
            'titles': sum(1 for post in posts if query.lower() in post.title.lower()),
            'categories': sum(1 for post in posts if post.category and query.lower() in post.category.name.lower()),
            'authors': sum(1 for post in posts if query.lower() in post.author.name.lower()),
            'tags': sum(1 for post in posts if any(query.lower() in tag.tag.name.lower() for tag in post.tags))
        }
    else:
        results_count = None

    return render_template('index.html',
                           all_posts=posts,
                           title=f'Search results for: {query}',
                           search_query=query,
                           results_count=results_count)


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    comments = Comment.query.filter_by(blog_id=post_id).all()

    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            comment = comment_form.data.get('body')
            new_comment = Comment(
                text=comment,
                author=current_user,
                blog=requested_post
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))
        else:
            flash("Please Log In")
            return redirect(url_for('login'))
    return render_template("post.html", post=requested_post, form=comment_form, comments=comments, gravatar=gravatar)


@app.route("/new-post", methods=["GET", "POST"])
@login_required
def add_new_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            category_id=form.category.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)

        # Add tags
        tag_names = form.tags.data.split(',')
        for name in tag_names:
            tag = Tag.query.filter_by(name=name.strip()).first()
            if not tag:
                tag = Tag(name=name.strip())
                db.session.add(tag)
            post_tag = PostTag(post=new_post, tag=tag)
            db.session.add(post_tag)

        db.session.commit()
        flash("Post created successfully with tags and category!")
        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)

    if current_user.id != post.author_id and current_user.id != 1:
        flash("You do not have permission to edit this post.")
        return redirect(url_for('get_all_posts'))

    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    edit_form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        flash("Post updated successfully.")
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    if current_user.id != post_to_delete.author_id and not current_user.id == 1:
        abort(403)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            message = request.form.get('message')

            if not name or not email or not message:
                flash("Please fill out all required fields.")

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL_USER, password=EMAIL_PASSWORD)
                content = f"Name- {name}\nEmail- {email}\nPhone- {phone}\nMessage- {message}\n"
                connection.sendmail(from_addr=EMAIL_USER, to_addrs=EMAIL_USER, msg=f"Subject::Message\n\n{content}")
                return render_template('contact.html', msg_sent=True)
        except Exception as e:
            return render_template('contact.html', msg_sent=False)

    return render_template("contact.html")


if __name__ == "__main__":
    app.run()
