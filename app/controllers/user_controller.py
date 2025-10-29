from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint("user", __name__, template_folder='../views')

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # TODO: Add additional user properties and update User model
        username = request.form.get('fullname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('signup.html', title='Signup page')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html', title='Signup page')

        try:
            # Create a new user
            user = User(username=username)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('user.login'))

        except IntegrityError:
            db.session.rollback()
            flash('Username already exists', 'error')
            return render_template('signup.html', title='Signup page')
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('signup.html', title='Signup page')

    # on GET request
    return render_template('signup.html', title='Signup page')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username

            flash('Logged in successfully!', 'success')
            return redirect(url_for('company.index'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html', title='Login page')

    # on GET request
    return render_template('login.html', title='Login page')


@user_bp.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('company.index'))