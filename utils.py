import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def parse_dates_robust(series):
    """Robust date parsing that handles multiple formats"""
    return pd.to_datetime(series, errors='coerce', dayfirst=True, format='mixed')


def intelligent_column_detection(df):
    """
    Intelligently detect ALL columns by semantic meaning and data type.
    Returns multiple candidates for each category, not just one.
    """
    detected = {
        'date_candidates': [],
        'customer_candidates': [],
        'product_candidates': [],
        'sales_candidates': [],
        'quantity_candidates': [],
        'price_candidates': [],
        'numeric_cols': [],
        'text_cols': [],
        'categorical_cols': []
    }
    
    # Basic type detection
    detected['numeric_cols'] = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(include=['string', 'object']).columns.tolist()
    detected['text_cols'] = text_cols.copy()
    
    # 1. DATE DETECTION - Find ALL date-like columns
    date_keywords = ['date', 'time', 'timestamp', 'day', 'month', 'year', 'when', 'created', 'updated', 'invoice', 'order', 'ship', 'purchase', 'sale', 'transaction']
    
    for col in text_cols:
        col_lower = col.lower()
        
        # Check if column name suggests it's a date
        is_date_name = any(keyword in col_lower for keyword in date_keywords)
        
        # Try to parse as date
        try:
            parsed = pd.to_datetime(df[col].dropna().iloc[:100], errors='coerce')
            successful_parses = parsed.notna().sum()
            
            # If >80% parse successfully, it's a date column
            if successful_parses > 80:
                detected['date_candidates'].append(col)
                if col in detected['text_cols']:
                    detected['text_cols'].remove(col)
        except:
            # Even if parsing fails, if name strongly suggests date, add it
            if is_date_name:
                detected['date_candidates'].append(col)
    
    # 2. CUSTOMER DETECTION - Find ALL customer-like columns
    customer_keywords = ['customer', 'client', 'buyer', 'purchaser', 'user', 'account', 'person', 'contact', 'name', 'shopper']
    
    for col in detected['text_cols']:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in customer_keywords):
            # Check if it has reasonable cardinality (not too many unique values)
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.8:  # Not every row is unique
                detected['customer_candidates'].append(col)
    
    # 3. PRODUCT DETECTION - Find ALL product-like columns
    product_keywords = ['product', 'item', 'sku', 'stock', 'goods', 'merchandise', 'article', 'description', 'category', 'brand']
    
    for col in detected['text_cols']:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in product_keywords):
            detected['product_candidates'].append(col)
    
    # 4. SALES/REVENUE DETECTION - Find ALL sales-like numeric columns
    sales_keywords = ['sales', 'revenue', 'amount', 'total', 'value', 'price', 'cost', 'sum', 'grand']
    
    for col in detected['numeric_cols']:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in sales_keywords):
            detected['sales_candidates'].append(col)
    
    # 5. QUANTITY DETECTION - Find ALL quantity-like columns
    quantity_keywords = ['quantity', 'qty', 'units', 'count', 'volume', 'number', 'amount']
    
    for col in detected['numeric_cols']:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in quantity_keywords):
            detected['quantity_candidates'].append(col)
    
    # 6. UNIT PRICE DETECTION - Find ALL price-per-unit columns
    price_keywords = ['price', 'unit', 'rate', 'cost', 'charge']
    
    for col in detected['numeric_cols']:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in price_keywords):
            if 'total' not in col_lower and 'sum' not in col_lower:
                detected['price_candidates'].append(col)
    
    # 7. CATEGORICAL DETECTION - Low cardinality text columns
    for col in detected['text_cols']:
        if col not in detected['customer_candidates'] and col not in detected['product_candidates']:
            if df[col].nunique() < len(df) * 0.5 and df[col].nunique() < 50:
                detected['categorical_cols'].append(col)
    
    return detected


def smart_column_mapper(df):
    """
    Pick the BEST candidate from each category for standardized names.
    Priority: most specific name match first.
    """
    column_map = {}
    columns_lower = {col.lower(): col for col in df.columns}
    
    # Date - pick Order Date first, then others
    date_priority = ['order_date', 'orderdate', 'invoice_date', 'invoicedate', 'date', 'transaction_date', 'sale_date', 'purchase_date', 'ship_date', 'created_at']
    for pattern in date_priority:
        if pattern in columns_lower:
            column_map['Date'] = columns_lower[pattern]
            break
    
    # Customer - pick Customer Name/ID first
    customer_priority = ['customer_name', 'customername', 'customer', 'customer_id', 'customerid', 'client', 'buyer', 'user']
    for pattern in customer_priority:
        if pattern in columns_lower:
            column_map['Customer'] = columns_lower[pattern]
            break
    
    # Product - pick Product Name first
    product_priority = ['product_name', 'productname', 'product', 'item_name', 'item', 'description', 'stock_code', 'sku']
    for pattern in product_priority:
        if pattern in columns_lower:
            column_map['Product'] = columns_lower[pattern]
            break
    
    # Sales - pick Total_Sales first
    sales_priority = ['total_sales', 'sales', 'revenue', 'total_revenue', 'amount', 'total_amount', 'value', 'price']
    for pattern in sales_priority:
        if pattern in columns_lower:
            column_map['Total_Sales'] = columns_lower[pattern]
            break
    
    # Quantity
    quantity_priority = ['quantity', 'qty', 'units', 'count']
    for pattern in quantity_priority:
        if pattern in columns_lower:
            column_map['Quantity'] = columns_lower[pattern]
            break
    
    # Unit Price
    price_priority = ['unit_price', 'unitprice', 'price', 'rate', 'cost']
    for pattern in price_priority:
        if pattern in columns_lower:
            column_map['UnitPrice'] = columns_lower[pattern]
            break
    
    return column_map


def apply_column_mapping(df, column_map):
    """
    Create standardized columns while preserving originals.
    Auto-calculates Total_Sales if possible.
    """
    df_mapped = df.copy()
    
    # Add mapped columns
    for standard_name, original_name in column_map.items():
        if original_name in df.columns and standard_name not in df.columns:
            df_mapped[standard_name] = df[original_name]
    
    # Calculate Total_Sales if not exists but Quantity and UnitPrice do
    if 'Total_Sales' not in df_mapped.columns:
        if 'Quantity' in df_mapped.columns and 'UnitPrice' in df_mapped.columns:
            df_mapped['Total_Sales'] = df_mapped['Quantity'] * df_mapped['UnitPrice']
    
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
    today = df['Date'].max()
    threshold_date = today - timedelta(days=days_threshold)
    
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
    
    top_3_revenue = product_revenue.head(3).sum()
    concentration_ratio = (top_3_revenue / total_revenue) * 100
    
    return {
        'product_revenue': product_revenue,
        'concentration_ratio': round(concentration_ratio, 2),
        'top_product': product_revenue.index[0] if len(product_revenue) > 0 else None,
        'top_product_revenue': product_revenue.iloc[0] if len(product_revenue) > 0 else 0
    }

def detect_revenue_decline_alerts(df, threshold_pct=-10):
    """Detect significant revenue declines"""
    df['Date'] = parse_dates_robust(df['Date'])
    
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total_Sales'].sum()
    
    if len(monthly_sales) < 2:
        return []
    
    alerts = []
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
    
    customer_stats['Customer_Lifetime_Days'] = (
        parse_dates_robust(customer_stats['Last_Purchase']) - 
        parse_dates_robust(customer_stats['First_Purchase'])
    ).dt.days
    
    customer_stats = customer_stats.sort_values('Total_Revenue', ascending=False)
    customer_stats['Rank'] = range(1, len(customer_stats) + 1)
    
    return customer_stats

def predict_churn_risk(df):
    """Simple rule-based churn prediction"""
    df['Date'] = parse_dates_robust(df['Date'])
    today = df['Date'].max()
    
    customer_stats = df.groupby('Customer').agg({
        'Date': ['max', 'count'],
        'Total_Sales': 'sum'
    }).reset_index()
    
    customer_stats.columns = ['Customer', 'Last_Purchase', 'Order_Count', 'Total_Revenue']
    customer_stats['Days_Since_Purchase'] = (today - parse_dates_robust(customer_stats['Last_Purchase'])).dt.days
    
    def calculate_risk(row):
        risk_score = 0
        if row['Days_Since_Purchase'] > 90:
            risk_score += 40
        elif row['Days_Since_Purchase'] > 60:
            risk_score += 30
        elif row['Days_Since_Purchase'] > 30:
            risk_score += 15
        
        if row['Order_Count'] < 5:
            risk_score += 30
        elif row['Order_Count'] < 10:
            risk_score += 15
        
        avg_revenue = customer_stats['Total_Revenue'].mean()
        if row['Total_Revenue'] < avg_revenue * 0.5:
            risk_score += 30
        elif row['Total_Revenue'] < avg_revenue * 0.8:
            risk_score += 15
        
        return min(risk_score, 100)
    
    customer_stats['Churn_Risk_Score'] = customer_stats.apply(calculate_risk, axis=1)
    
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
    """Generate automated KPIs"""
    df['Date'] = parse_dates_robust(df['Date'])
    
    kpis = {
        'total_revenue': df['Total_Sales'].sum(),
        'total_orders': len(df),
        'avg_order_value': df['Total_Sales'].mean(),
        'unique_customers': df['Customer'].nunique() if 'Customer' in df.columns else 0,
        'date_range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
        'data_quality_score': round((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 1)
    }
    
    monthly_growth = calculate_monthly_growth(df)
    kpis['monthly_growth'] = monthly_growth
    
    if 'Product' in df.columns:
        kpis['total_products'] = df['Product'].nunique()
        product_dep = analyze_product_dependency(df)
        if product_dep:
            kpis['top_product'] = product_dep['top_product']
            kpis['product_concentration'] = product_dep['concentration_ratio']
    
    return kpis
