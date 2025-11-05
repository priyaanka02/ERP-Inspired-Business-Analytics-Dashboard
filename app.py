app-FIXED.py
# ERP-Inspired Business Analytics Dashboard
# Enhanced with Revenue Alerts, Churn Prediction & SAP-Style KPIs

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import enhanced utilities
from utils import (
    calculate_monthly_growth,
    detect_churn_customers,
    analyze_product_dependency,
    detect_revenue_decline_alerts,
    calculate_customer_metrics,
    predict_churn_risk,
    generate_kpi_summary,
    smart_column_mapper,
    apply_column_mapping
)

# Page configuration
st.set_page_config(
    page_title="🏢 ERP Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-responsive and SAP-style design
st.markdown("""
<style>
    /* SAP-Inspired Color Scheme */
    :root {
        --sap-blue: #0070F2;
        --sap-green: #30914C;
        --sap-orange: #E76500;
        --sap-red: #BB0000;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0070F2 0%, #005ECC 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #0070F2;
        margin-bottom: 1rem;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0070F2;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .alert-high {
        background: #FFF3F3;
        border-left: 4px solid #BB0000;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .alert-medium {
        background: #FFF8E1;
        border-left: 4px solid #E76500;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: #F1F8F4;
        border-left: 4px solid #30914C;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .kpi-card {
            padding: 1rem;
        }
        .kpi-value {
            font-size: 1.5rem;
        }
    }
    
    /* Status indicators */
    .status-active {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #30914C;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

def smart_data_detection(df):
    """Intelligently detect data types and suggest columns"""
    df = df.convert_dtypes()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    date_cols = []
    text_cols = df.select_dtypes(include=['string', 'object']).columns.tolist()
    
    # Smart date detection
    for col in text_cols.copy():
        try:
            pd.to_datetime(df[col].dropna().iloc[:100])
            date_cols.append(col)
            text_cols.remove(col)
        except:
            pass
    
    # Detect potential categorical columns (low cardinality)
    categorical_cols = [col for col in text_cols if df[col].nunique() < len(df) * 0.5 and df[col].nunique() < 50]
    
    return {
        'numeric': numeric_cols,
        'date': date_cols,
        'text': text_cols,
        'categorical': categorical_cols
    }

def display_kpi_cards(kpis):
    """Display SAP-style KPI cards with proper currency formatting"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Get currency symbol from KPIs
    currency = kpis.get('currency_symbol', '$')
    
    with col1:
        # Use the pre-formatted value from utils (already has correct currency)
        revenue_display = kpis.get('total_revenue_formatted', f"{currency}0")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💰 Total Revenue</div>
            <div class="kpi-value">{revenue_display}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        growth_color = "#30914C" if kpis['monthly_growth'] >= 0 else "#BB0000"
        growth_icon = "📈" if kpis['monthly_growth'] >= 0 else "📉"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{growth_icon} Monthly Growth</div>
            <div class="kpi-value" style="color: {growth_color}">{kpis['monthly_growth']:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📦 Total Orders</div>
            <div class="kpi-value">{kpis['total_orders']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">👥 Customers</div>
            <div class="kpi-value">{kpis['unique_customers']}</div>
        </div>
        """, unsafe_allow_html=True)

def display_alerts(alerts):
    """Display revenue decline alerts"""
    if not alerts:
        st.markdown("""
        <div class="success-box">
            ✅ <strong>No Critical Alerts</strong> - Revenue performance is healthy
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("### ⚠️ Revenue Alerts")
    for alert in alerts:
        alert_class = "alert-high" if alert['severity'] == 'High' else "alert-medium"
        severity_icon = "🚨" if alert['severity'] == 'High' else "⚠️"
        
        st.markdown(f"""
        <div class="{alert_class}">
            {severity_icon} <strong>{alert['type']}</strong> ({alert['severity']} Priority)<br>
            {alert['message']}<br>
            <small>Current: {alert['current_value']} | Previous: {alert['previous_value']}</small>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏢 ERP-Inspired Business Analytics Dashboard</h1>
        <p style="margin: 0;">SAP-Style Reporting with Real-Time Insights | <span class="status-active"></span> Live</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'last_upload_time' not in st.session_state:
        st.session_state.last_upload_time = None
    
    # Sidebar
    st.sidebar.markdown("## 📂 Data Upload")
    st.sidebar.markdown("Upload your business data (CSV/Excel)")
    
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls'],
        help="Supports CSV and Excel formats"
    )
    
    # Load demo data option
    use_demo = st.sidebar.checkbox("📊 Use Demo Data (10,000+ records)", value=False)
    
    # Handle file upload or demo data
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state.df = df
            st.session_state.last_upload_time = datetime.now()
            st.sidebar.success(f"✅ Loaded {len(df):,} records")
            
        except Exception as e:
            st.sidebar.error(f"Error loading file: {str(e)}")
            return
    
    elif use_demo:
        # Load sample data
        try:
            df = pd.read_csv('sample_data.csv')
            st.session_state.df = df
            st.sidebar.success(f"✅ Loaded {len(df):,} demo records")
        except:
            st.sidebar.error("Demo data file not found")
            return
    
    # Main content
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        
        # Display upload time
        if st.session_state.last_upload_time:
            upload_time = st.session_state.last_upload_time.strftime("%Y-%m-%d %H:%M:%S")
            st.sidebar.info(f"🕐 Last updated: {upload_time}")
        
        # Smart column mapping
        column_map = smart_column_mapper(df)
        df = apply_column_mapping(df, column_map)

        # Show column mapping results with detailed feedback
        with st.sidebar.expander("🔍 Column Detection Results", expanded=True):
            if column_map:
                st.success(f"✅ Successfully auto-mapped {len(column_map)} columns")
                for standard, original in column_map.items():
                    st.write(f"**{standard}** ← `{original}`")
            else:
                st.warning("⚠️ No standard columns auto-detected")

            # Show what's missing
            required_for_features = {
                'KPIs': ['Date', 'Total_Sales'],
                'Alerts': ['Date', 'Total_Sales'],
                'Churn Prediction': ['Customer', 'Date', 'Total_Sales'],
                'Product Analysis': ['Product', 'Total_Sales']
            }

            missing_features = []
            for feature, required in required_for_features.items():
                missing = [col for col in required if col not in df.columns]
                if missing:
                    missing_features.append((feature, missing))

            if missing_features:
                st.info("ℹ️ **Features with limited data:**")
                for feature, missing_cols in missing_features:
                    st.write(f"• {feature}: missing `{', '.join(missing_cols)}`")

        # Detect columns
        detected = smart_data_detection(df)

        
        # Generate KPIs
        st.markdown("## 📊 Key Performance Indicators")
        
        try:
            kpis = generate_kpi_summary(df)
            display_kpi_cards(kpis)
            
            # Additional KPI details
            col1, col2, col3 = st.columns(3)
            with col1:
                # Use pre-formatted value with correct currency
                avg_order_display = kpis.get('avg_order_value_formatted', 
                                            f"{kpis.get('currency_symbol', '$')}{kpis.get('avg_order_value', 0):,.2f}")
                st.metric("Average Order Value", avg_order_display)
            with col2:
                if 'total_products' in kpis:
                    st.metric("Products", kpis['total_products'])
            with col3:
                st.metric("Data Quality", f"{kpis['data_quality_score']}%")
            
        except Exception as e:
            st.info("📊 KPIs require Date and Total_Sales columns. Upload data with date and sales/revenue columns.")
        
        # Revenue Decline Alerts
        st.markdown("---")
        st.markdown("## 🚨 Real-Time Business Alerts")
        
        try:
            alerts = detect_revenue_decline_alerts(df)
            display_alerts(alerts)
        except Exception as e:
            st.info("🚨 Revenue alerts require Date and Total_Sales columns for time-series analysis.")
        
        # Churn Prediction
        st.markdown("---")
        st.markdown("## 🎯 Customer Churn Prediction")
        
        try:
            churn_data = predict_churn_risk(df)
            
            # Display high-risk customers
            high_risk = churn_data[churn_data['Risk_Category'] == 'High']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🔴 High Risk", len(high_risk))
            with col2:
                medium_risk = churn_data[churn_data['Risk_Category'] == 'Medium']
                st.metric("🟡 Medium Risk", len(medium_risk))
            with col3:
                low_risk = churn_data[churn_data['Risk_Category'] == 'Low']
                st.metric("🟢 Low Risk", len(low_risk))
            
            # Show top at-risk customers
            if len(high_risk) > 0:
                st.markdown("### Top At-Risk Customers")
                display_churn = high_risk[['Customer', 'Churn_Risk_Score', 'Days_Since_Purchase', 'Total_Revenue']].head(10)
                st.dataframe(display_churn, use_container_width=True)
            
            # Churn risk distribution chart
            fig = px.histogram(
                churn_data,
                x='Churn_Risk_Score',
                color='Risk_Category',
                title='Churn Risk Distribution',
                labels={'Churn_Risk_Score': 'Risk Score', 'count': 'Number of Customers'},
                color_discrete_map={'High': '#BB0000', 'Medium': '#E76500', 'Low': '#30914C'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.info(f"Churn prediction requires Customer, Date, and Total_Sales columns")
        
        # Data Visualization Section
        st.markdown("---")
        st.markdown("## 📈 Interactive Visualizations")
        
        tabs = st.tabs(["📊 Time Series", "📉 Distributions", "🔗 Correlations", "🎯 Categories"])
        
        # Time Series Tab
        with tabs[0]:
            if detected['date'] and detected['numeric']:
                date_col = st.selectbox("Select Date Column", detected['date'], key='ts_date')
                metric_col = st.selectbox("Select Metric", detected['numeric'], key='ts_metric')
                
                df[date_col] = pd.to_datetime(df[date_col])
                time_series = df.groupby(df[date_col].dt.to_period('D'))[metric_col].sum().reset_index()
                time_series[date_col] = time_series[date_col].astype(str)
                
                fig = px.line(
                    time_series,
                    x=date_col,
                    y=metric_col,
                    title=f'{metric_col} Over Time',
                    labels={metric_col: metric_col, date_col: 'Date'}
                )
                fig.update_traces(line_color='#0070F2', line_width=2)
                fig.update_layout(hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Upload data with date and numeric columns for time series analysis")
        
        # Distributions Tab
        with tabs[1]:
            if detected['numeric']:
                num_col = st.selectbox("Select Column", detected['numeric'], key='dist_col')
                
                fig = px.histogram(
                    df,
                    x=num_col,
                    title=f'Distribution of {num_col}',
                    marginal='box',
                    color_discrete_sequence=['#0070F2']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mean", f"{df[num_col].mean():.2f}")
                with col2:
                    st.metric("Median", f"{df[num_col].median():.2f}")
                with col3:
                    st.metric("Std Dev", f"{df[num_col].std():.2f}")
                with col4:
                    st.metric("Range", f"{df[num_col].max() - df[num_col].min():.2f}")
            else:
                st.info("No numeric columns found")
        
               # Correlations Tab
        with tabs[2]:
            if len(detected['numeric']) >= 2:
                # Create sub-tabs for scatter plot and heatmap
                subtab1, subtab2 = st.tabs(["📊 Scatter Plot", "🔥 Correlation Heatmap"])
                
                with subtab1:
                    x_col = st.selectbox("X-Axis", detected['numeric'], key='corr_x')
                    y_col = st.selectbox("Y-Axis", [col for col in detected['numeric'] if col != x_col], key='corr_y')
                    
                    fig = px.scatter(
                        df,
                        x=x_col,
                        y=y_col,
                        title=f'{x_col} vs {y_col}',
                        color_discrete_sequence=['#0070F2']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    corr = df[x_col].corr(df[y_col])
                    st.metric("Correlation Coefficient", f"{corr:.3f}")
                
                with subtab2:
                    st.markdown("### 🔥 Correlation Matrix")
                    
                    numeric_df = df[detected['numeric']]
                    corr_matrix = numeric_df.corr()
                    
                    fig = px.imshow(
                        corr_matrix,
                        text_auto='.2f',
                        aspect="auto",
                        title="Correlation Heatmap",
                        color_continuous_scale='RdBu_r',
                        zmin=-1,
                        zmax=1
                    )
                    fig.update_layout(height=600)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info("🔴 Red = Positive | ⚪ White = None | 🔵 Blue = Negative")
            else:
                st.info("Need at least 2 numeric columns for correlation analysis")


        
        # Categories Tab
        with tabs[3]:
            if detected['categorical']:
                cat_col = st.selectbox("Select Category", detected['categorical'], key='cat_col')
        
                if detected['numeric']:
                    metric_col = st.selectbox("Select Metric", detected['numeric'], key='cat_metric')
            
                    cat_data = df.groupby(cat_col)[metric_col].sum().sort_values(ascending=False).head(10)
            
                    # Bar chart and pie chart side by side
                    col1, col2 = st.columns(2)
            
                    with col1:
                        fig = px.bar(
                            x=cat_data.index,
                            y=cat_data.values,
                            title=f'Top 10 {cat_col} by {metric_col}',
                            labels={'x': cat_col, 'y': metric_col},
                            color=cat_data.values,
                            color_continuous_scale='Blues'
                            )
                        st.plotly_chart(fig, use_container_width=True)
            
                    with col2:
                        fig = px.pie(
                            values=cat_data.values,
                            names=cat_data.index,
                            title=f'{cat_col} Distribution',
                            color_discrete_sequence=px.colors.sequential.Blues_r,
                            hole=0.3
                        )
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No categorical columns found")

        
        # Data Preview
        st.markdown("---")
        st.markdown("## 🔍 Data Preview")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Dataset:** {len(df):,} rows × {len(df.columns)} columns")
        with col2:
            show_rows = st.number_input("Rows to display", 5, 100, 10)
        
        st.dataframe(df.head(show_rows), use_container_width=True)
        
        # Download processed data
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Processed Data (CSV)",
            data=csv,
            file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    else:
        # Welcome screen
        st.markdown("""
        ## 👋 Welcome to the ERP Business Analytics Dashboard
        
        ### Features:
        - 📊 **Automated KPI Generation** - Revenue, growth, customer metrics
        - 🚨 **Real-Time Alerts** - Revenue decline detection
        - 🎯 **Churn Prediction** - Identify at-risk customers
        - 📈 **Interactive Charts** - Mobile-responsive visualizations
        - 💾 **Session Persistence** - Data stays loaded during your session
        - 📥 **Export Reports** - Download processed data
        
        ### Getting Started:
        1. Upload your CSV/Excel file using the sidebar
        2. Or check "Use Demo Data" to see it in action
        3. Explore automated insights and visualizations
        
        ### Data Requirements:
        - **Recommended columns**: Date, Customer, Product, Total_Sales
        - **Supports**: 10,000+ records
        - **Formats**: CSV, Excel (.xlsx, .xls)
        """)
        
        st.info("💡 Tip: The dashboard automatically detects your data structure and creates appropriate visualizations!")

if __name__ == "__main__":
    main()
