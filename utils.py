import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def parse_dates_robust(series):
    """Robust date parsing that handles dd/mm/yyyy format (like Superstore data)"""
    return pd.to_datetime(series, errors='coerce', dayfirst=True, format='mixed')


def smart_column_mapper(df):
    """
    Intelligently map common column name variations to standard names.
    Returns a dictionary of standardized mappings.
    """
    column_map = {}
    columns_lower = {col.lower(): col for col in df.columns}
    
    # Date column patterns
    date_patterns = ['date', 'order_date', 'orderdate', 'ship_date', 'shipdate', 
                     'order date', 'invoice_date', 'invoicedate', 'transaction_date',
                     'sale_date', 'purchase_date', 'created_at']
    
    for pattern in date_patterns:
        if pattern in columns_lower:
            column_map['Date'] = columns_lower[pattern]
            break
    
    # Customer column patterns
    customer_patterns = ['customer', 'customer_name', 'customername', 'customer name',
                        'client', 'client_name', 'customer_id', 'customerid',
                        'buyer', 'purchaser', 'person']
    
    for pattern in customer_patterns:
        if pattern in columns_lower:
            column_map['Customer'] = columns_lower[pattern]
            break
    
    # Product column patterns
    product_patterns = ['product', 'product_name', 'productname', 'product name',
                       'item', 'item_name', 'description', 'category']
    
    for pattern in product_patterns:
        if pattern in columns_lower:
            column_map['Product'] = columns_lower[pattern]
            break
    
    # Sales/Revenue column patterns (most important!)
    sales_patterns = ['total_sales', 'totalsales', 'total sales', 'sales', 'revenue',
                     'total_revenue', 'amount', 'total_amount', 'value', 'price']
    
    for pattern in sales_patterns:
        if pattern in columns_lower:
            column_map['Total_Sales'] = columns_lower[pattern]
            break
    
    return column_map


def apply_column_mapping(df, column_map):
    """
    Create a copy of dataframe with standardized column names.
    """
    df_mapped = df.copy()
    
    for standard_name, original_name in column_map.items():
        if original_name in df.columns and standard_name not in df.columns:
            df_mapped[standard_name] = df[original_name]
    
    return df_mapped


def calculate_monthly_growth(df):
    """Calculate month-over-month growth percentage"""
    df['Date'] = parse_dates_robust(df['Date'])
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total_Sales'].sum()
    
    if len(monthly_sales) < 2:
        return 0.0
    
    current_month = monthly_sales.iloc[-1]
    previous_month = monthly_sales.iloc[-2]
    
    if previous_month == 0:
        return 0.0
    
    growth = ((current_month - previous_month) / previous_month) * 100
    return round(growth, 2)

def detect_churn_customers(df, days_threshold=60):
    """Detect customers who haven't purchased in the last N days"""
    df['Date'] = parse_dates_robust(df['Date'])
    today = df['Date'].max()  # Use latest date in dataset
    threshold_date = today - timedelta(days=days_threshold)
    
    # Get last purchase date for each customer
    last_purchase = df.groupby('Customer')['Date'].max()
    churned_customers = last_purchase[last_purchase < threshold_date]
    
    return churned_customers.index.tolist(), len(churned_customers)

def analyze_product_dependency(df):
    """Analyze revenue concentration by product"""
    if 'Product' not in df.columns or 'Total_Sales' not in df.columns:
        return None
    
    product_revenue = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
    total_revenue = product_revenue.sum()
    
    if total_revenue == 0:
        return None
    
    # Calculate concentration ratio (top 3 products)
    top_3_revenue = product_revenue.head(3).sum()
    concentration_ratio = (top_3_revenue / total_revenue) * 100
    
    return {
        'product_revenue': product_revenue,
        'concentration_ratio': round(concentration_ratio, 2),
        'top_product': product_revenue.index[0] if len(product_revenue) > 0 else None,
        'top_product_revenue': product_revenue.iloc[0] if len(product_revenue) > 0 else 0
    }

def detect_revenue_decline_alerts(df, threshold_pct=-10):
    """Detect significant revenue declines (SAP-style alerts)"""
    df['Date'] = parse_dates_robust(df['Date'])
    
    # Monthly revenue trend
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total_Sales'].sum()
    
    if len(monthly_sales) < 2:
        return []
    
    alerts = []
    
    # Check recent month vs previous month
    current_month = monthly_sales.iloc[-1]
    previous_month = monthly_sales.iloc[-2]
    
    if previous_month > 0:
        change_pct = ((current_month - previous_month) / previous_month) * 100
        
        if change_pct <= threshold_pct:
            alerts.append({
                'type': 'Revenue Decline',
                'severity': 'High' if change_pct <= -20 else 'Medium',
                'message': f'Monthly revenue declined by {abs(change_pct):.1f}%',
                'current_value': f'${current_month:,.2f}',
                'previous_value': f'${previous_month:,.2f}'
            })
    
    # Check for negative growth trend (3+ months)
    if len(monthly_sales) >= 3:
        recent_trend = monthly_sales.tail(3).pct_change().mean() * 100
        if recent_trend < -5:
            alerts.append({
                'type': 'Negative Trend',
                'severity': 'Medium',
                'message': f'3-month revenue trend declining by {abs(recent_trend):.1f}% on average',
                'current_value': f'${monthly_sales.iloc[-1]:,.2f}',
                'previous_value': f'${monthly_sales.iloc[-3]:,.2f}'
            })
    
    return alerts

def calculate_customer_metrics(df):
    """Calculate customer-level performance metrics"""
    if 'Customer' not in df.columns or 'Total_Sales' not in df.columns:
        return None
    
    customer_stats = df.groupby('Customer').agg({
        'Total_Sales': ['sum', 'count', 'mean'],
        'Date': ['min', 'max']
    }).reset_index()
    
    customer_stats.columns = ['Customer', 'Total_Revenue', 'Order_Count', 'Avg_Order_Value', 'First_Purchase', 'Last_Purchase']
    
    # Calculate customer lifetime (days)
    customer_stats['Customer_Lifetime_Days'] = (
        parse_dates_robust(customer_stats['Last_Purchase']) - 
        parse_dates_robust(customer_stats['First_Purchase'])
    ).dt.days
    
    # Rank customers
    customer_stats = customer_stats.sort_values('Total_Revenue', ascending=False)
    customer_stats['Rank'] = range(1, len(customer_stats) + 1)
    
    return customer_stats

def predict_churn_risk(df):
    """Simple rule-based churn prediction (no ML libraries needed)"""
    df['Date'] = parse_dates_robust(df['Date'])
    today = df['Date'].max()
    
    customer_stats = df.groupby('Customer').agg({
        'Date': ['max', 'count'],
        'Total_Sales': 'sum'
    }).reset_index()
    
    customer_stats.columns = ['Customer', 'Last_Purchase', 'Order_Count', 'Total_Revenue']
    
    # Calculate days since last purchase
    customer_stats['Days_Since_Purchase'] = (today - parse_dates_robust(customer_stats['Last_Purchase'])).dt.days
    
    # Simple risk scoring (0-100)
    # Higher score = higher churn risk
    def calculate_risk(row):
        risk_score = 0
        
        # Factor 1: Days since last purchase (0-40 points)
        if row['Days_Since_Purchase'] > 90:
            risk_score += 40
        elif row['Days_Since_Purchase'] > 60:
            risk_score += 30
        elif row['Days_Since_Purchase'] > 30:
            risk_score += 15
        
        # Factor 2: Order frequency (0-30 points)
        if row['Order_Count'] < 5:
            risk_score += 30
        elif row['Order_Count'] < 10:
            risk_score += 15
        
        # Factor 3: Revenue value (0-30 points) - low value = higher risk
        avg_revenue = customer_stats['Total_Revenue'].mean()
        if row['Total_Revenue'] < avg_revenue * 0.5:
            risk_score += 30
        elif row['Total_Revenue'] < avg_revenue * 0.8:
            risk_score += 15
        
        return min(risk_score, 100)
    
    customer_stats['Churn_Risk_Score'] = customer_stats.apply(calculate_risk, axis=1)
    
    # Categorize risk
    def categorize_risk(score):
        if score >= 70:
            return 'High'
        elif score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    customer_stats['Risk_Category'] = customer_stats['Churn_Risk_Score'].apply(categorize_risk)
    
    return customer_stats.sort_values('Churn_Risk_Score', ascending=False)

def generate_kpi_summary(df):
    """Generate automated KPIs (SAP-style dashboard metrics)"""
    df['Date'] = parse_dates_robust(df['Date'])
    
    kpis = {
        'total_revenue': df['Total_Sales'].sum(),
        'total_orders': len(df),
        'avg_order_value': df['Total_Sales'].mean(),
        'unique_customers': df['Customer'].nunique() if 'Customer' in df.columns else 0,
        'date_range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
        'data_quality_score': round((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 1)
    }
    
    # Calculate growth
    monthly_growth = calculate_monthly_growth(df)
    kpis['monthly_growth'] = monthly_growth
    
    # Product analysis
    if 'Product' in df.columns:
        kpis['total_products'] = df['Product'].nunique()
        product_dep = analyze_product_dependency(df)
        if product_dep:
            kpis['top_product'] = product_dep['top_product']
            kpis['product_concentration'] = product_dep['concentration_ratio']
    
    return kpis
