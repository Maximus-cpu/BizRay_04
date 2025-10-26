from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__, template_folder='../views')

@main_bp.route('/')
def index():
    return render_template('index.html', title='Home page')