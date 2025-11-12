"""
Financial Risk Indicator Calculator

This module calculates financial risk indicators based on company financial data.
Each indicator returns a score from 0-100, where higher scores indicate better financial health.
"""

from typing import Dict, Optional, Any


class FinancialRiskCalculator:
    """Calculates financial risk indicators and their scores."""
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    def calculate_working_capital(self, current_assets: float, current_liabilities: float) -> Dict[str, Any]:
        """
        Calculate Working Capital.
        
        Formula: working_capital = current_assets - current_liabilities
        
        Args:
            current_assets: Current assets value
            current_liabilities: Current liabilities value
            
        Returns:
            Dictionary with 'value' and 'score' (score used as fallback for color coding)
        """
        if current_assets is None or current_liabilities is None:
            return {"value": None, "score": 0}
        
        working_capital = current_assets - current_liabilities
        
        # Simple scoring: positive = good, negative = bad (used as fallback for color coding)
        score = 100 if working_capital > 0 else 20
        
        return {
            "value": working_capital,
            "score": score
        }
    
    def calculate_liquidity_ratio(self, current_assets: float, current_liabilities: float) -> Dict[str, Any]:
        """
        Calculate Liquidity Ratio (Current Ratio) and its risk score.
        
        Formula: liquidity_ratio = current_assets / current_liabilities
        
        Args:
            current_assets: Current assets value
            current_liabilities: Current liabilities value
            
        Returns:
            Dictionary with 'value' and 'score' (0-100)
        """
        if current_assets is None or current_liabilities is None or current_liabilities == 0:
            return {"value": None, "score": 0}
        
        liquidity_ratio = current_assets / current_liabilities
        
        # Scoring logic:
        if liquidity_ratio >= 2:
            score = 100
        elif liquidity_ratio >= 1.8:
            score = 90
        elif liquidity_ratio >= 1.5:
            score = 80
        elif liquidity_ratio >= 1.3:
            score = 70
        elif liquidity_ratio >= 1:
            score = 60
        elif liquidity_ratio >= 0.5:
            score = 50
        elif liquidity_ratio >= 0.2:
            score = 40
        elif liquidity_ratio >= 0.1:
            score = 30
        elif liquidity_ratio >= 0.05:
            score = 20
        else:
            score = 10
        
        return {
            "value": liquidity_ratio,
            "score": score
        }
    
    def calculate_equity_ratio(self, equity: float, total_assets: float) -> Dict[str, Any]:
        """
        Calculate Equity Ratio and its risk score.
        
        Formula: equity_ratio = equity / total_assets
        
        Args:
            equity: Equity value
            total_assets: Total assets (Balance Sheet Total)
            
        Returns:
            Dictionary with 'value' and 'score' (0-100)
        """
        if equity is None or total_assets is None or total_assets == 0:
            return {"value": None, "score": 0}
        
        equity_ratio = equity / total_assets
        
        # Detailed scoring for slider display (needs granular scores for visual representation)
        if equity_ratio >= 0.5:
            score = 100
        elif equity_ratio >= 0.4:
            score = 90
        elif equity_ratio >= 0.35:
            score = 80
        elif equity_ratio >= 0.3:
            score = 70
        elif equity_ratio >= 0.25:
            score = 60
        elif equity_ratio >= 0.2:
            score = 50
        elif equity_ratio >= 0.15:
            score = 40
        elif equity_ratio >= 0.1:
            score = 30
        elif equity_ratio >= 0.05:
            score = 20
        else:
            score = 10
        
        return {
            "value": equity_ratio,
            "score": score
        }
    
    def calculate_debt_ratio(self, liabilities: float, total_assets: float) -> Dict[str, Any]:
        """
        Calculate Debt Ratio.
        
        Formula: debt_ratio = liabilities / total_assets
        
        Args:
            liabilities: Total liabilities value
            total_assets: Total assets (Balance Sheet Total)
            
        Returns:
            Dictionary with 'value' and 'score' (score used as fallback for color coding)
        """
        if liabilities is None or total_assets is None or total_assets == 0:
            return {"value": None, "score": 0}
        
        debt_ratio = liabilities / total_assets
        
        # Simplified scoring (inverse: lower is better)
        # Used as fallback for color coding; primary color logic is value-based in JavaScript
        if debt_ratio <= 0.5:
            score = 100
        elif debt_ratio <= 1:
            score = 70
        else:
            score = 20
        
        return {
            "value": debt_ratio,
            "score": score
        }
    
    def calculate_coverage_fixed_assets(self, equity: float, fixed_assets: float) -> Dict[str, Any]:
        """
        Calculate Coverage of Fixed Assets I.
        
        Formula: coverage_fixed_assets = equity / fixed_assets
        
        Args:
            equity: Equity value
            fixed_assets: Fixed assets value
            
        Returns:
            Dictionary with 'value' and 'score' (score used as fallback for color coding)
        """
        if equity is None or fixed_assets is None or fixed_assets == 0:
            return {"value": None, "score": 0}
        
        coverage_fixed_assets = equity / fixed_assets
        
        # Simplified scoring (used as fallback for color coding; primary color logic is value-based)
        if coverage_fixed_assets >= 1:
            score = 100
        elif coverage_fixed_assets >= 0.8:
            score = 80
        else:
            score = 40
        
        return {
            "value": coverage_fixed_assets,
            "score": score
        }
    
    def calculate_liquidity_I(self, cash_equivalents: Optional[float], current_liabilities: float, current_assets: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate Liquidity I (Cash Ratio) and its risk score.
        
        Formula: liquidity_I = cash_equivalents / current_liabilities
        
        Note: If cash_equivalents is not available, we'll estimate it as a portion of current_assets
        (typically 20-30% of current assets are cash/cash equivalents).
        
        Args:
            cash_equivalents: Cash and cash equivalents (optional, can be None)
            current_liabilities: Current liabilities value
            current_assets: Current assets value (used as fallback if cash_equivalents is None)
            
        Returns:
            Dictionary with 'value' and 'score' (0-100)
        """
        if current_liabilities is None or current_liabilities == 0:
            return {"value": None, "score": 0}
        
        # If cash_equivalents is not available, estimate it from current_assets
        if cash_equivalents is None:
            if current_assets is not None and current_assets > 0:
                # Estimate cash_equivalents as 25% of current_assets (typical range is 20-30%)
                cash_equivalents = current_assets * 0.25
            else:
                # Cannot calculate without cash_equivalents or current_assets
                return {"value": None, "score": 30}
        
        liquidity_I = cash_equivalents / current_liabilities
        
        # Scoring logic: >= 1 = 100, >= 0.2 = 70, < 0.2 = 30
        if liquidity_I >= 1:
            score = 100
        elif liquidity_I >= 0.8:
            score = 90
        elif liquidity_I >= 0.7:
            score = 80 
        elif liquidity_I >= 0.6:
            score = 70
        elif liquidity_I >= 0.5:
            score = 60
        elif liquidity_I >= 0.4:
            score = 50
        elif liquidity_I >= 0.3:
            score = 40
        elif liquidity_I >= 0.2:
            score = 30
        elif liquidity_I >= 0.1:
            score = 20
        else:
            score = 10
        
        return {
            "value": liquidity_I,
            "score": score
        }
    
    def calculate_profit_margin(self, current_year_result: float, total_assets: float) -> Dict[str, Any]:
        """
        Calculate Profit Margin (Scaled).
        
        Formula: profit_margin = current_year_result / total_assets
        
        Args:
            current_year_result: Current year result (profit/loss)
            total_assets: Total assets (Balance Sheet Total)
            
        Returns:
            Dictionary with 'value' and 'score' (score used as fallback for color coding)
        """
        if current_year_result is None or total_assets is None or total_assets == 0:
            return {"value": None, "score": 0}
        
        profit_margin = current_year_result / total_assets
        
        # Simplified scoring (used as fallback for color coding; primary color logic is value-based)
        if profit_margin > 0.1:
            score = 100
        elif profit_margin > 0:
            score = 80
        else:
            score = 30
        
        return {
            "value": profit_margin,
            "score": score
        }
    
    def calculate_all_indicators(self, financial_data: Dict[str, Optional[float]]) -> Dict[str, Dict[str, Any]]:
        """
        Calculate all financial risk indicators from financial data.
        
        Expected financial_data keys:
            - balance_sheet_total (total_assets)
            - fixed_assets
            - current_assets
            - prepaid_expenses
            - equity
            - provisions
            - liabilities
            - balance_sheet_profit
            - retained_earnings
            - current_year_result
            - cash_equivalents (optional)
            - current_liabilities (if not provided, will be estimated from liabilities)
        
        Args:
            financial_data: Dictionary containing financial values
            
        Returns:
            Dictionary with all indicator results, each containing 'value' and 'score'
        """
        # Extract values with defaults
        total_assets = financial_data.get("balance_sheet_total")
        fixed_assets = financial_data.get("fixed_assets")
        current_assets = financial_data.get("current_assets")
        equity = financial_data.get("equity")
        liabilities = financial_data.get("liabilities")
        current_year_result = financial_data.get("current_year_result")
        cash_equivalents = financial_data.get("cash_equivalents")
        
        # Estimate current_liabilities if not provided
        # For now, we'll use a portion of liabilities or current_assets as fallback
        current_liabilities = financial_data.get("current_liabilities")
        if current_liabilities is None:
            # If not provided, estimate as a portion of total liabilities
            # This is a simplification - in real scenarios, you'd need the actual short-term portion
            if liabilities is not None and current_assets is not None:
                # Rough estimate: assume 60% of liabilities are current (short-term)
                # Note: This is an estimation. In real financial statements, you would have
                # the actual breakdown of current vs long-term liabilities.
                # If you want to use 100% of liabilities as current, change 0.6 to 1.0
                current_liabilities = liabilities * 0.6
            else:
                current_liabilities = None
        
        results = {
            "working_capital": self.calculate_working_capital(current_assets, current_liabilities),
            "liquidity_ratio": self.calculate_liquidity_ratio(current_assets, current_liabilities),
            "equity_ratio": self.calculate_equity_ratio(equity, total_assets),
            "debt_ratio": self.calculate_debt_ratio(liabilities, total_assets),
            "coverage_fixed_assets": self.calculate_coverage_fixed_assets(equity, fixed_assets),
            "liquidity_I": self.calculate_liquidity_I(cash_equivalents, current_liabilities, current_assets),
            "profit_margin": self.calculate_profit_margin(current_year_result, total_assets)
        }
        
        return results


# Convenience function for easy usage
def calculate_financial_risk_indicators(financial_data: Dict[str, Optional[float]]) -> Dict[str, Dict[str, Any]]:
    """
    Convenience function to calculate all financial risk indicators.
    
    Args:
        financial_data: Dictionary containing financial values
        
    Returns:
        Dictionary with all indicator results
    """
    calculator = FinancialRiskCalculator()
    return calculator.calculate_all_indicators(financial_data)

