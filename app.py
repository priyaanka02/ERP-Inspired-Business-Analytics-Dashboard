import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import our custom utilities
from utils import (calculate_monthly_growth, detect_churn_customers, 
                  analyze_product_dependency, generate_business_insights,
                  format_currency, format_number)

# Page configuration
st.set_page_config(
    page_title="ERP Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_data(uploaded_file=None):
    """Load data from uploaded file or sample data"""
    try:
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv('sample_data.csv')

        # Ensure proper data types
        df['Date'] = pd.to_datetime(df['Date'])
        df['Total_Sales'] = pd.to_numeric(df['Total_Sales'], errors='coerce')

        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def main():
    # Header Section
    st.markdown('<h1 class="main-header">🏢 ERP-Inspired Business Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Streamlit-powered analytics tool simulating SAP-style sales reporting with real-time insights</p>', 
                unsafe_allow_html=True)

    # Sidebar for file upload and filters
    st.sidebar.title("📁 Data Management")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Sales Data (CSV/Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your sales data or use the sample dataset"
    )

    # Load data
    df = load_data(uploaded_file)

    if df is None:
        st.error("❌ Failed to load data. Please check your file format.")
        st.stop()

    # Data validation
    required_columns = ['Date', 'Customer', 'Product', 'Quantity', 'Price', 'Total_Sales']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"❌ Missing required columns: {missing_columns}")
        st.info("Required columns: Date, Customer, Product, Quantity, Price, Total_Sales")
        st.stop()

    # Sidebar filters
    st.sidebar.title("🔍 Filters")

    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['Date'].min(), df['Date'].max()),
        min_value=df['Date'].min(),
        max_value=df['Date'].max()
    )

    # Customer filter
    customers = st.sidebar.multiselect(
        "Select Customers",
        options=sorted(df['Customer'].unique()),
        default=sorted(df['Customer'].unique())
    )

    # Product filter
    products = st.sidebar.multiselect(
        "Select Products",
        options=sorted(df['Product'].unique()),
        default=sorted(df['Product'].unique())
    )

    # Apply filters
    if len(date_range) == 2:
        df_filtered = df[
            (df['Date'] >= pd.to_datetime(date_range[0])) &
            (df['Date'] <= pd.to_datetime(date_range[1])) &
            (df['Customer'].isin(customers)) &
            (df['Product'].isin(products))
        ]
    else:
        df_filtered = df[
            (df['Customer'].isin(customers)) &
            (df['Product'].isin(products))
        ]

    if df_filtered.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your selection.")
        st.stop()

    # KPI Section - Row 1
    st.markdown("## 📈 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_revenue = df_filtered['Total_Sales'].sum()
        st.metric(
            label="💰 Total Revenue",
            value=format_currency(total_revenue),
            delta=f"{len(df_filtered)} orders"
        )

    with col2:
        top_product = df_filtered.groupby('Product')['Total_Sales'].sum().idxmax()
        top_product_revenue = df_filtered.groupby('Product')['Total_Sales'].sum().max()
        st.metric(
            label="🏆 Top-Selling Product",
            value=top_product.split(' - ')[1] if ' - ' in top_product else top_product,
            delta=format_currency(top_product_revenue)
        )

    with col3:
        top_customer = df_filtered.groupby('Customer')['Total_Sales'].sum().idxmax()
        top_customer_revenue = df_filtered.groupby('Customer')['Total_Sales'].sum().max()
        st.metric(
            label="🎯 Best Customer",
            value=top_customer,
            delta=format_currency(top_customer_revenue)
        )

    with col4:
        monthly_growth = calculate_monthly_growth(df_filtered)
        st.metric(
            label="📊 Monthly Growth",
            value=f"{monthly_growth:+.1f}%",
            delta="Month-over-Month"
        )

    # Visualizations - Row 2
    st.markdown("## 📊 Sales Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Sales trend over time
        daily_sales = df_filtered.groupby('Date')['Total_Sales'].sum().reset_index()
        fig_line = px.line(
            daily_sales, 
            x='Date', 
            y='Total_Sales',
            title='📈 Sales Trend Over Time',
            labels={'Total_Sales': 'Revenue ($)', 'Date': 'Date'},
            template='plotly_white'
        )
        fig_line.update_traces(line_color='#1f77b4', line_width=3)
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        # Top 5 products bar chart
        top_products = df_filtered.groupby('Product')['Total_Sales'].sum().nlargest(5).reset_index()
        top_products['Product_Short'] = top_products['Product'].str.split(' - ').str[1]

        fig_bar = px.bar(
            top_products,
            x='Product_Short',
            y='Total_Sales',
            title='🏆 Top 5 Products by Revenue',
            labels={'Total_Sales': 'Revenue ($)', 'Product_Short': 'Product'},
            template='plotly_white',
            color='Total_Sales',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Revenue by customer pie chart
    st.markdown("### 🎯 Revenue Distribution by Customer")
    customer_revenue = df_filtered.groupby('Customer')['Total_Sales'].sum().nlargest(8).reset_index()

    fig_pie = px.pie(
        customer_revenue,
        values='Total_Sales',
        names='Customer',
        title='Revenue Share by Top 8 Customers',
        template='plotly_white'
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=500)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Business Insights - Row 3
    st.markdown("## 🧠 AI-Powered Business Insights")

    insights = generate_business_insights(df_filtered)

    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

    # Additional Analytics
    st.markdown("## 📋 Detailed Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Customer Performance")
        customer_stats = df_filtered.groupby('Customer').agg({
            'Total_Sales': ['sum', 'count', 'mean']
        }).round(2)
        customer_stats.columns = ['Total Revenue', 'Orders', 'Avg Order Value']
        customer_stats = customer_stats.sort_values('Total Revenue', ascending=False)
        st.dataframe(customer_stats, use_container_width=True)

    with col2:
        st.subheader("📦 Product Performance")
        product_stats = df_filtered.groupby('Product').agg({
            'Total_Sales': ['sum', 'count'],
            'Quantity': 'sum'
        }).round(2)
        product_stats.columns = ['Total Revenue', 'Orders', 'Units Sold']
        product_stats = product_stats.sort_values('Total Revenue', ascending=False)
        st.dataframe(product_stats, use_container_width=True)

    # Raw data view
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df_filtered.sort_values('Date', ascending=False), use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>🚀 ERP Analytics Dashboard - Built with Streamlit | 
        📊 Powered by Python, Pandas & Plotly | 
        💼 Ready for Enterprise Deployment</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
