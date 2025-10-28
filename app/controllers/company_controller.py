from flask import Blueprint, render_template, request

company_bp = Blueprint("company", __name__, template_folder='../views')

@company_bp.route('/')
def index():
    return render_template('index.html', title='Home page')

@company_bp.route('/search')
def search():
    # Get query parameters from the URL
    company_name = request.args.get('company_name')
    company_id = request.args.get('fnr')

    # Filter database results based on query parameters
    results = []

    if company_name:
        # Search by company name
        from app.models.company import Company
        results = Company.query.filter(Company.name.like(f'%{company_name}%')).all()
    elif company_id:
        # Search by company ID
        from app.models.company import Company
        results = Company.query.filter_by(id=company_id).first()

    return render_template('search.html',
        title='Search page',
        results=results,
        company_name=company_name,
        company_id=company_id
    )

@company_bp.route('/company/<company_id>')
def company_details(company_id):
    return render_template('company_details.html',
                           title='Company details page',
                           company_id=company_id
    )