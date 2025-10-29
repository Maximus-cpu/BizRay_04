from flask import Blueprint, render_template, request, abort

from app.models.company import Company

company_bp = Blueprint("company", __name__, template_folder='../views')

@company_bp.route('/')
def index():
    from app.models.company import Company
    from app.models.user import User
    company_count = Company.query.count()
    user_count = User.query.count()
    return render_template('index.html',
                           title='Home page',
                           company_count=company_count,
                           user_count=user_count)

@company_bp.route('/search')
def search():
    from app.models.company import Company
    from sqlalchemy import and_

    # Allowed query params
    allowed_params = {'company_name', 'fnr', 'industry', 'company_size', 'page'}
    filter_params = {'company_name', 'fnr', 'industry', 'company_size'}
    provided_params = set(request.args.keys())

    # Validate query params
    invalid_params = provided_params - allowed_params
    if invalid_params:
        abort(400, description=f"Invalid query parameter(s): {', '.join(invalid_params)}")

    # Determine if any search parameters were provided (exclude pagination)
    search_performed = any(request.args.get(param) for param in filter_params)

    # Unpack parameters
    company_name = request.args.get('company_name', '').strip()
    fnr = request.args.get('fnr')
    industry = request.args.getlist('industry')
    company_size = request.args.getlist('company_size')

    results = []
    pagination = None
    filters = []

    # Apply filters based on provided parameters
    if company_name:
        filters.append(Company.name.ilike(f"%{company_name}%"))
    if industry:
        filters.append(Company.industry.in_(industry))
    if company_size:
        filters.append(Company.employees_count.between(*map(int, company_size[0].split('-')))
                       if '-' in company_size[0]
                       else Company.employees_count >= int(company_size[0].replace('+', '')))
    if fnr:
        filters.append(Company.id == fnr)

    # Apply combined filters if they exist
    if filters:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = 10
        query = Company.query.filter(and_(*filters))
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        results = pagination.items

    return render_template(
        'search.html',
        title='Search page',
        results=results,
        company_name=company_name,
        selected_industries=industry,
        selected_sizes=company_size,
        search_performed=search_performed,
        pagination=pagination
    )

@company_bp.route('/company/<company_id>')
def company_details(company_id):
    from app.models.company import Company

    # Query the specific company by ID
    company = Company.query.get(company_id)

    # Show 404 error if the company is not found
    if not company:
        abort(404)

    return render_template('company_details.html',
                           title=f'{company.name} • Details',
                           company=company
                           )