import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def parse_dates_robust(series):
    """Robust date parsing that handles multiple formats"""
    return pd.to_datetime(series, errors='coerce', dayfirst=True, format='mixed')

def smart_column_mapper(df):
    """
    COMPREHENSIVE column mapper that recognizes ANY common business column name.
    Covers: e-commerce, retail, SaaS, B2B, financial, analytics datasets.
    """
    column_map = {}
    columns_lower = {col.lower(): col for col in df.columns}

    # ============================================
    # DATE COLUMNS - Exhaustive patterns
    # ============================================
    date_priority = [
        # Order/Transaction dates
        'order_date', 'orderdate', 'order date',
        'transaction_date', 'transactiondate', 'transaction date',
        'purchase_date', 'purchasedate', 'purchase date',
        'sale_date', 'saledate', 'sale date',
        'invoice_date', 'invoicedate', 'invoice date',
        'billing_date', 'billingdate', 'billing date',
        'payment_date', 'paymentdate', 'payment date',
        # Shipping dates
        'ship_date', 'shipdate', 'ship date',
        'shipping_date', 'shippingdate', 'shipping date',
        'delivery_date', 'deliverydate', 'delivery date',
        'shipped_date', 'shippeddate', 'shipped date',
        # System dates
        'created_at', 'createdat', 'created at', 'created',
        'updated_at', 'updatedat', 'updated at', 'updated',
        'modified_at', 'modifiedat', 'modified at', 'modified',
        'date_created', 'datecreated', 'date created',
        'date_added', 'dateadded', 'date added',
        # Generic date columns
        'date', 'datetime', 'timestamp', 'time',
        'dt', 'day', 'event_date', 'eventdate',
        # Period dates
        'period', 'period_date', 'perioddate',
        'week', 'week_date', 'weekdate',
        'month', 'month_date', 'monthdate',
        'year', 'fiscal_date', 'fiscaldate'
    ]

    for pattern in date_priority:
        if pattern in columns_lower:
            column_map['Date'] = columns_lower[pattern]
            break

    # ============================================
    # CUSTOMER COLUMNS - Exhaustive patterns
    # ============================================
    customer_priority = [
        # Customer names
        'customer_name', 'customername', 'customer name',
        'client_name', 'clientname', 'client name',
        'buyer_name', 'buyername', 'buyer name',
        'purchaser_name', 'purchasername', 'purchaser name',
        'account_name', 'accountname', 'account name',
        'contact_name', 'contactname', 'contact name',
        # Customer IDs
        'customer_id', 'customerid', 'customer id',
        'client_id', 'clientid', 'client id',
        'buyer_id', 'buyerid', 'buyer id',
        'account_id', 'accountid', 'account id',
        'user_id', 'userid', 'user id',
        # Generic customer terms
        'customer', 'client', 'buyer', 'purchaser',
        'user', 'username', 'user name', 'member',
        'subscriber', 'account', 'person', 'contact',
        # Email/Phone (can identify customers)
        'email', 'customer_email', 'customeremail',
        'phone', 'customer_phone', 'customerphone'
    ]

    for pattern in customer_priority:
        if pattern in columns_lower:
            column_map['Customer'] = columns_lower[pattern]
            break

    # ============================================
    # PRODUCT COLUMNS - Exhaustive patterns
    # ============================================
    product_priority = [
        # Product names
        'product_name', 'productname', 'product name',
        'item_name', 'itemname', 'item name',
        'goods_name', 'goodsname', 'goods name',
        'article_name', 'articlename', 'article name',
        # Product IDs/Codes
        'product_id', 'productid', 'product id',
        'item_id', 'itemid', 'item id',
        'sku', 'sku_code', 'skucode', 'sku code',
        'stock_code', 'stockcode', 'stock code',
        'upc', 'barcode', 'gtin', 'asin',
        # Descriptions
        'description', 'product_description', 'productdescription',
        'item_description', 'itemdescription',
        'product_details', 'productdetails',
        # Generic product terms
        'product', 'item', 'goods', 'merchandise',
        'article', 'variant', 'offering',
        # Categories (can represent products)
        'category', 'product_category', 'productcategory',
        'subcategory', 'product_type', 'producttype',
        'brand', 'manufacturer', 'model'
    ]

    for pattern in product_priority:
        if pattern in columns_lower:
            column_map['Product'] = columns_lower[pattern]
            break

    # ============================================
    # SALES/REVENUE COLUMNS - Exhaustive patterns
    # ============================================
    sales_priority = [
        # Total sales variations
        'total_sales', 'totalsales', 'total sales',
        'total_revenue', 'totalrevenue', 'total revenue',
        'gross_sales', 'grosssales', 'gross sales',
        'net_sales', 'netsales', 'net sales',
        # Period sales
        'weekly_sales', 'weeklysales', 'weekly sales',
        'daily_sales', 'dailysales', 'daily sales',
        'monthly_sales', 'monthlysales', 'monthly sales',
        'quarterly_sales', 'quarterlysales', 'quarterly sales',
        'annual_sales', 'annualsales', 'annual sales',
        'yearly_sales', 'yearlysales', 'yearly sales',
        # Generic sales/revenue
        'sales', 'revenue', 'income', 'earnings',
        # Amount variations
        'total_amount', 'totalamount', 'total amount',
        'grand_total', 'grandtotal', 'grand total',
        'net_amount', 'netamount', 'net amount',
        'gross_amount', 'grossamount', 'gross amount',
        'amount', 'sum', 'total',
        # Value variations
        'total_value', 'totalvalue', 'total value',
        'order_value', 'ordervalue', 'order value',
        'transaction_value', 'transactionvalue', 'transaction value',
        'sale_value', 'salevalue', 'sale value',
        'value',
        # Price variations
        'price', 'total_price', 'totalprice', 'total price',
        'sale_price', 'saleprice', 'sale price',
        'selling_price', 'sellingprice', 'selling price',
        # Cost variations (sometimes used for revenue)
        'cost', 'total_cost', 'totalcost', 'total cost'
    ]

    for pattern in sales_priority:
        if pattern in columns_lower:
            column_map['Total_Sales'] = columns_lower[pattern]
            break

    # ============================================
    # QUANTITY COLUMNS
    # ============================================
    quantity_priority = [
        'quantity', 'qty', 'quantities',
        'order_quantity', 'orderquantity', 'order quantity',
        'sold_quantity', 'soldquantity', 'sold quantity',
        'units', 'units_sold', 'unitssold', 'units sold',
        'count', 'item_count', 'itemcount', 'item count',
        'volume', 'number', 'amount'
    ]

    for pattern in quantity_priority:
        if pattern in columns_lower:
            column_map['Quantity'] = columns_lower[pattern]
            break

    # ============================================
    # UNIT PRICE COLUMNS
    # ============================================
    price_priority = [
        'unit_price', 'unitprice', 'unit price',
        'price_per_unit', 'priceperunit', 'price per unit',
        'item_price', 'itemprice', 'item price',
        'product_price', 'productprice', 'product price',
        'list_price', 'listprice', 'list price',
        'base_price', 'baseprice', 'base price',
        'price', 'rate', 'unit_cost', 'unitcost'
    ]

    for pattern in price_priority:
        if pattern in columns_lower:
            # Don't map if it's already mapped to Total_Sales
            if columns_lower[pattern] != column_map.get('Total_Sales'):
                column_map['UnitPrice'] = columns_lower[pattern]
                break

    return column_map

def apply_column_mapping(df, column_map):
    """
    Apply standardized column names while preserving originals.
    Auto-calculates Total_Sales if possible.
    """
    df_mapped = df.copy()

    # Add mapped columns
    for standard_name, original_name in column_map.items():
        if original_name in df.columns and standard_name not in df.columns:
            df_mapped[standard_name] = df[original_name]

    # Parse Date column if it exists
    if 'Date' in df_mapped.columns:
        df_mapped['Date'] = parse_dates_robust(df_mapped['Date'])

    # Auto-calculate Total_Sales if Quantity and UnitPrice exist
    if 'Total_Sales' not in df_mapped.columns:
        if 'Quantity' in df_mapped.columns and 'UnitPrice' in df_mapped.columns:
            try:
                df_mapped['Total_Sales'] = pd.to_numeric(df_mapped['Quantity'], errors='coerce') * pd.to_numeric(df_mapped['UnitPrice'], errors='coerce')
            except Exception:
                pass

    # Ensure numeric columns are properly typed
    if 'Total_Sales' in df_mapped.columns:
        df_mapped['Total_Sales'] = pd.to_numeric(df_mapped['Total_Sales'], errors='coerce')
    if 'Quantity' in df_mapped.columns:
        df_mapped['Quantity'] = pd.to_numeric(df_mapped['Quantity'], errors='coerce')
    if 'UnitPrice' in df_mapped.columns:
        df_mapped['UnitPrice'] = pd.to_numeric(df_mapped['UnitPrice'], errors='coerce')

    return df_mapped

def validate_required_columns(df, required_columns):
    """
    Validate that required columns exist and have valid data.
    Returns tuple: (is_valid, missing_columns, empty_columns)
    """
    missing = [col for col in required_columns if col not in df.columns]
    empty = [col for col in required_columns if col in df.columns and df[col].isna().all()]
    is_valid = len(missing) == 0 and len(empty) == 0
    return is_valid, missing, empty

def calculate_monthly_growth(df):
    """Calculate month-over-month growth percentage"""
    is_valid, missing, empty = validate_required_columns(df, ['Date', 'Total_Sales'])
    if not is_valid:
        return None

    try:
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
    except Exception:
        return None

def detect_churn_customers(df, days_threshold=60):
    """Detect customers who haven't purchased in the last N days"""
    is_valid, missing, empty = validate_required_columns(df, ['Date', 'Customer'])
    if not is_valid:
        return [], 0

    try:
        df['Date'] = parse_dates_robust(df['Date'])
        today = df['Date'].max()
        threshold_date = today - timedelta(days=days_threshold)

        last_purchase = df.groupby('Customer')['Date'].max()
        churned_customers = last_purchase[last_purchase < threshold_date]

        return churned_customers.index.tolist(), len(churned_customers)
    except Exception:
        return [], 0

def analyze_product_dependency(df):
    """Analyze revenue concentration by product"""
    is_valid, missing, empty = validate_required_columns(df, ['Product', 'Total_Sales'])
    if not is_valid:
        return None

    try:
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
    except Exception:
        return None

def detect_revenue_decline_alerts(df, threshold_pct=-10):
    """Detect significant revenue declines"""
    is_valid, missing, empty = validate_required_columns(df, ['Date', 'Total_Sales'])
    if not is_valid:
        return []

    try:
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
    except Exception:
        return []

def calculate_customer_metrics(df):
    """Calculate customer-level performance metrics"""
    is_valid, missing, empty = validate_required_columns(df, ['Customer', 'Total_Sales', 'Date'])
    if not is_valid:
        return None

    try:
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
    except Exception:
        return None

def predict_churn_risk(df):
    """Simple rule-based churn prediction"""
    is_valid, missing, empty = validate_required_columns(df, ['Customer', 'Date', 'Total_Sales'])
    if not is_valid:
        return None

    try:
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
    except Exception:
        return None

def generate_kpi_summary(df):
    """Generate automated KPIs with flexible column support"""
    kpis = {}

    # Basic KPIs that don't require specific columns
    kpis['total_orders'] = len(df)
    kpis['data_quality_score'] = round((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 1)

    # Date-dependent KPIs
    if 'Date' in df.columns:
        try:
            df['Date'] = parse_dates_robust(df['Date'])
            valid_dates = df['Date'].dropna()
            if len(valid_dates) > 0:
                kpis['date_range'] = f"{valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}"
        except Exception:
            pass

    # Sales/Revenue KPIs
    if 'Total_Sales' in df.columns:
        try:
            kpis['total_revenue'] = df['Total_Sales'].sum()
            kpis['avg_order_value'] = df['Total_Sales'].mean()
        except Exception:
            pass

    # Customer KPIs
    if 'Customer' in df.columns:
        try:
            kpis['unique_customers'] = df['Customer'].nunique()
        except Exception:
            kpis['unique_customers'] = 0
    else:
        kpis['unique_customers'] = 0

    # Growth calculation
    growth = calculate_monthly_growth(df)
    if growth is not None:
        kpis['monthly_growth'] = growth
    else:
        kpis['monthly_growth'] = 0

    # Product KPIs
    if 'Product' in df.columns:
        try:
            kpis['total_products'] = df['Product'].nunique()
            product_dep = analyze_product_dependency(df)
            if product_dep:
                kpis['top_product'] = product_dep['top_product']
                kpis['product_concentration'] = product_dep['concentration_ratio']
        except Exception:
            pass

    return kpis
