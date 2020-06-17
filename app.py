"""Flask Feedback App"""

from flask import Flask, render_template, redirect, session
from models import connect_db, db, User, Feedback
from forms import LoginForm, RegistrationForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "asdf1234"

connect_db(app)

@app.route("/")
def home():
    """Home page, redirect to register"""
    return redirect("/register")

@app.route("/register", methods=['GET', 'POST'])
def registration_page():
    """Show registration form to create a user or redirect to userpage if they're already logged in"""

        if "username" in session:
        return redirect(f"/users/{session['username']}")

        form = RegistrationForm()

        if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        User.register(username, password, first_name, last_name, email)

        session['username'] = username

        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    """Show login page to log in a user or redirect to userpage if they're already logged in"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = username
            return redirect(f"/users/{username}")
        else:
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Handle logging out a user"""

    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>")
def userpage():
    """Render a userpage if the person logged in is the user"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)

    return render_template("user_info.html", user=user)

@app.route("/users/<username>/delete", methods=['POST'])
def delete_user():
    """Deletes a user from database and all their feedback"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback():
    """Add feedback to userpage"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        add_feedback(title, content, username)

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback_form.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """Edit feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback_form.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/update", methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")


