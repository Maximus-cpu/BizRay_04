from flask import Blueprint, render_template, request, abort, jsonify

company_bp = Blueprint("company", __name__, template_folder='../views')

@company_bp.route('/')
def index():
    from app.models.company import Company
    from app.models.user import User
    company_count = Company.query.count()
    user_count = User.query.count()
    return render_template('index.html',
                           title='BizRay - Find Business Information',
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

@company_bp.route('/search_suggest')
def search_suggest():
    from app.models.company import Company
    prefix = request.args.get('prefix', '').strip()
    if not prefix:
        return jsonify({"suggestions": []})

    suggestions = (
        Company.query
        .filter(Company.name.ilike(f"{prefix}%"))
        .order_by(Company.name.asc())
        .limit(5)
        .with_entities(Company.name)
        .all()
    )

    names = [name for (name,) in suggestions]
    return jsonify({"suggestions": names})

@company_bp.route('/api/calculate_financial_risk', methods=['POST'])
def calculate_financial_risk():
    """
    API endpoint to calculate financial risk indicators.
    
    Expects JSON body with financial data:
    {
        "balance_sheet_total": float,
        "fixed_assets": float,
        "current_assets": float,
        "prepaid_expenses": float,
        "equity": float,
        "provisions": float,
        "liabilities": float,
        "balance_sheet_profit": float,
        "retained_earnings": float,
        "current_year_result": float,
        "cash_equivalents": float (optional),
        "current_liabilities": float (optional)
    }
    
    Returns JSON with risk scores for each indicator (0-100).
    """
    from app.services.financial_risk_calculator import calculate_financial_risk_indicators
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Convert string values to float, handle "—" or empty values as None
        def parse_value(value):
            if value is None or value == "" or value == "—" or value == "-":
                return None
            try:
                if isinstance(value, str):
                    # Remove spaces first
                    cleaned = value.replace(" ", "")
                    
                    # Count separators
                    dot_count = cleaned.count(".")
                    comma_count = cleaned.count(",")
                    
                    # Handle European format: dots as thousand separators (e.g., "10.000.000.000")
                    if dot_count > 1:
                        # Multiple dots = thousand separators, remove all
                        cleaned = cleaned.replace(".", "")
                    # Handle US format: commas as thousand separators (e.g., "10,000,000,000")
                    elif comma_count > 1:
                        # Multiple commas = thousand separators, remove all
                        cleaned = cleaned.replace(",", "")
                    # Handle single separator - could be decimal or thousand
                    elif dot_count == 1:
                        # Check position: if dot is in last 3 chars, likely decimal (e.g., "1.5", "10.50")
                        last_dot_pos = cleaned.rfind(".")
                        if last_dot_pos >= len(cleaned) - 3:
                            # Keep as decimal separator
                            pass
                        else:
                            # Likely thousand separator, remove it
                            cleaned = cleaned.replace(".", "")
                    elif comma_count == 1:
                        # European decimal format (comma as decimal)
                        last_comma_pos = cleaned.rfind(",")
                        if last_comma_pos >= len(cleaned) - 3:
                            # Convert comma to dot for decimal
                            cleaned = cleaned.replace(",", ".")
                        else:
                            # Likely thousand separator, remove it
                            cleaned = cleaned.replace(",", "")
                    
                    return float(cleaned)
                return float(value)
            except (ValueError, TypeError) as e:
                # Log error for debugging
                print(f"Error parsing value '{value}': {e}")
                return None
        
        financial_data = {
            "balance_sheet_total": parse_value(data.get("balance_sheet_total")),
            "fixed_assets": parse_value(data.get("fixed_assets")),
            "current_assets": parse_value(data.get("current_assets")),
            "prepaid_expenses": parse_value(data.get("prepaid_expenses")),
            "equity": parse_value(data.get("equity")),
            "provisions": parse_value(data.get("provisions")),
            "liabilities": parse_value(data.get("liabilities")),
            "balance_sheet_profit": parse_value(data.get("balance_sheet_profit")),
            "retained_earnings": parse_value(data.get("retained_earnings")),
            "current_year_result": parse_value(data.get("current_year_result")),
            "cash_equivalents": parse_value(data.get("cash_equivalents")),
            "current_liabilities": parse_value(data.get("current_liabilities"))
        }
        
        # Calculate all indicators
        results = calculate_financial_risk_indicators(financial_data)
        
        # Format response with both scores and values
        response = {
            "working_capital": {
                "score": results["working_capital"]["score"],
                "value": results["working_capital"]["value"]
            },
            "liquidity_ratio": {
                "score": results["liquidity_ratio"]["score"],
                "value": results["liquidity_ratio"]["value"]
            },
            "equity_ratio": {
                "score": results["equity_ratio"]["score"],
                "value": results["equity_ratio"]["value"]
            },
            "debt_ratio": {
                "score": results["debt_ratio"]["score"],
                "value": results["debt_ratio"]["value"]
            },
            "coverage_fixed_assets": {
                "score": results["coverage_fixed_assets"]["score"],
                "value": results["coverage_fixed_assets"]["value"]
            },
            "liquidity_I": {
                "score": results["liquidity_I"]["score"],
                "value": results["liquidity_I"]["value"]
            },
            "profit_margin": {
                "score": results["profit_margin"]["score"],
                "value": results["profit_margin"]["value"]
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500