from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
import re
from datetime import datetime, timezone

user_bp = Blueprint("user", __name__, template_folder='../views')

def validate_email_format(email):
    """Server-side email validation"""
    if not email:
        return False
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email.strip()) is not None

def validate_password_strength(password):
    """Server-side password strength validation"""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")

    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")

    return errors

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('firstname', '').strip()
        last_name = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        terms_checkbox = request.form.get('termsCheckbox', 'off') == 'on'

        # Server-side validation
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('signup.html', title='Sign Up', email=email)

        # Validate email format
        if not validate_email_format(email):
            flash('Invalid email format', 'error')
            return render_template('signup.html', title='Sign Up', email=email)

        # Validate password match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html', title='Sign Up', email=email)

        # Validate password strength
        password_errors = validate_password_strength(password)
        if password_errors:
            for error in password_errors:
                flash(error, 'error')
            return render_template('signup.html', title='Sign Up', email=email)

        # Validate terms and conditions checkbox
        if not terms_checkbox:
            flash('Please accept the terms and conditions', 'error')

        try:
            # Check if email already exists
            existing_user = User.query.filter_by(email=email.lower()).first()
            if existing_user:
                flash('An account with this email already exists', 'error')
                return render_template('signup.html', title='Sign Up', email=email)

            # Create a new user
            user = User(email=email.lower(), first_name=first_name or None, last_name=last_name or None)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('user.login'))

        except IntegrityError:
            db.session.rollback()
            flash('An account with this email already exists', 'error')
            return render_template('signup.html', title='Sign Up', email=email)
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('signup.html', title='Sign Up', email=email)
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return render_template('signup.html', title='Sign Up', email=email)

    # GET request
    return render_template('signup.html', title='Sign Up')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'

        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html', title='Log In', email=email)

        # Validate email format
        if not validate_email_format(email):
            flash('Invalid email format', 'error')
            return render_template('login.html', title='Log In', email=email)

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Invalid email or password', 'error')
            return render_template('login.html', title='Log In', email=email)

        # Check if the account is locked
        if user.is_account_locked():
            minutes_remaining = int((user.account_locked_until - datetime.now(timezone.utc)).total_seconds() / 60)
            flash(
                f'Account is temporarily locked due to multiple failed login attempts. Please try again in {minutes_remaining} minutes.',
                'error')
            return render_template('login.html', title='Log In', email=email)

        # Check password
        if user.check_password(password):
            # Successful login
            user.reset_failed_attempts()

            # Store user info in session
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['last_activity'] = datetime.now(timezone.utc).isoformat()

            # Set session to permanent if remember me is checked
            if remember_me:
                session.permanent = True
            else:
                session.permanent = False

            flash('Logged in successfully!', 'success')
            return redirect(url_for('company.index'))
        else:
            # Failed login
            user.record_failed_login()

            remaining_attempts = 3 - user.failed_login_attempts
            if remaining_attempts > 0:
                flash(f'Invalid email or password. {remaining_attempts} attempts remaining.', 'error')
            else:
                flash('Account locked due to multiple failed login attempts. Please try again in 15 minutes.', 'error')

            return render_template('login.html', title='Log In', email=email)

    # GET request
    return render_template('login.html', title='Log In')

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('company.index'))

@user_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        if not email or not validate_email_format(email):
            flash('Please enter a valid email address', 'error')
            return render_template('forgot_password.html', title='Forgot Password')

        user = User.query.filter_by(email=email).first()

        flash('If an account exists with this email, password reset instructions have been sent.', 'success')

        # TODO: Implement actual password reset token generation and email sending
        # For now, just redirect to login
        return redirect(url_for('user.login'))

    return render_template('forgot_password.html', title='Forgot Password')

@user_bp.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        session.clear()
        flash('Account deleted successfully.', 'success')
    return redirect(url_for('company.index'))

@user_bp.route('/account')
def account():
    if 'user_id' not in session:
        flash('Please log in to access your account', 'error')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('User not found', 'error')
        return redirect(url_for('user.login'))

    return render_template('account.html', title='Account Settings', user=user)