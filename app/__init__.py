from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv() # Upload environment variables

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from app.models.company import Company
    from app.models.user import User
    # Create an instance folder for the local test database
    # import os if you want to create the instance folder
    # instance_path = os.path.join(os.getcwd(), 'instance')
    # os.makedirs(instance_path, exist_ok=True)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.config.Config")

    # Set max session lifetime when a user remembers their password
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.company_controller import company_bp
    from app.controllers.user_controller import user_bp

    app.register_blueprint(company_bp)
    app.register_blueprint(user_bp)

    # Session expiration check before each request
    @app.before_request
    def check_session_expiration():
        """Check if the session has expired before each request"""
        from flask import session, request, redirect, url_for, flash
        from datetime import datetime, timezone, timedelta

        # Skip check for routes that don't require authentication
        if request.endpoint and request.endpoint in ['user.login', 'user.signup', 'user.forgot_password', 'static']:
            return None

        # Check if the user is logged in
        if 'user_id' in session:
            last_activity = session.get('last_activity')

            if last_activity:
                last_activity_time = datetime.fromisoformat(last_activity)
                current_time = datetime.now(timezone.utc)

                if session.permanent:
                    pass
                else:
                    # 2 hours expiration for non-permanent sessions
                    time_elapsed = current_time - last_activity_time
                    # TODO: CHANGE DEFAULT SESSION TIME TO LONGER AFTER DEMONSTRATION
                    if time_elapsed > timedelta(seconds=10):
                        session.clear()
                        flash('Your session has expired, please log in again.', 'error')
                        return redirect(url_for('user.login'))

            # Update last activity time
            session['last_activity'] = datetime.now(timezone.utc).isoformat()
        return None

    return app