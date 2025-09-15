import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_monthly_growth(df):
    """Calculate month-over-month growth percentage"""
    df['Date'] = pd.to_datetime(df['Date'])
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
    df['Date'] = pd.to_datetime(df['Date'])
    today = datetime.now()
    threshold_date = today - timedelta(days=days_threshold)

    # Get last purchase date for each customer
    last_purchase = df.groupby('Customer')['Date'].max()
    churned_customers = last_purchase[last_purchase < threshold_date]

    return churned_customers.index.tolist()

def analyze_product_dependency(df, threshold=40):
    """Identify products contributing more than threshold% of revenue"""
    total_revenue = df['Total_Sales'].sum()
    product_revenue = df.groupby('Product')['Total_Sales'].sum()
    product_percentage = (product_revenue / total_revenue) * 100

    high_dependency = product_percentage[product_percentage > threshold]
    return high_dependency.to_dict()

def generate_business_insights(df):
    """Generate rule-based business recommendations"""
    insights = []

    # Monthly growth analysis
    growth = calculate_monthly_growth(df)
    if growth < -10:
        insights.append("🚨 Alert: Revenue declined by {:.1f}% month-over-month. Consider promotional campaigns.".format(abs(growth)))
    elif growth > 20:
        insights.append("🚀 Excellent: Revenue grew by {:.1f}% month-over-month. Scale successful strategies.".format(growth))

    # Product dependency analysis
    dependencies = analyze_product_dependency(df)
    for product, percentage in dependencies.items():
        insights.append("⚠️ Risk: {} contributes {:.1f}% of total revenue. Consider portfolio diversification.".format(product, percentage))

    # Churn detection
    churned = detect_churn_customers(df)
    if churned:
        insights.append("📞 Action: {} customers haven't purchased in 60+ days. Initiate retention campaigns.".format(len(churned)))

    # Low performance check
    df['Date'] = pd.to_datetime(df['Date'])
    recent_sales = df[df['Date'] >= (datetime.now() - timedelta(days=30))]['Total_Sales'].sum()
    if recent_sales == 0:
        insights.append("📊 Note: No recent sales data available. Check data pipeline connectivity.")

    if not insights:
        insights.append("✅ Performance: All key metrics are within normal ranges. Continue monitoring trends.")

    return insights

def format_currency(amount):
    """Format number as currency"""
    return "${:,.2f}".format(amount)

def format_number(number):
    """Format large numbers with K/M suffixes"""
    if number >= 1000000:
        return "{:.1f}M".format(number / 1000000)
    elif number >= 1000:
        return "{:.1f}K".format(number / 1000)
    else:
        return str(int(number))
