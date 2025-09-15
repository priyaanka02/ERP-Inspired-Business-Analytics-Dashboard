import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🏢 ERP-Powered Universal Business Analytics Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def smart_data_detection(df):
    """Intelligently detect data types and suggest columns"""

    # Convert to best dtypes automatically
    df = df.convert_dtypes()

    # Detect column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    date_cols = []
    text_cols = df.select_dtypes(include=['string', 'object']).columns.tolist()

    # Smart date detection
    for col in text_cols.copy():
        # Try to convert to datetime
        try:
            pd.to_datetime(df[col].dropna().iloc[:100])  # Test first 100 rows
            date_cols.append(col)
            text_cols.remove(col)
        except:
            pass

    # Detect potential ID columns (mostly unique values)
    id_cols = []
    for col in df.columns:
        if df[col].nunique() / len(df) > 0.95 and col.lower() in ['id', 'index', 'key']:
            id_cols.append(col)

    # Detect potential categorical columns
    categorical_cols = []
    for col in text_cols:
        if df[col].nunique() < len(df) * 0.1:  # Less than 10% unique values
            categorical_cols.append(col)

    return {
        'numeric_cols': numeric_cols,
        'date_cols': date_cols, 
        'text_cols': text_cols,
        'categorical_cols': categorical_cols,
        'id_cols': id_cols
    }

def create_smart_visualizations(df, col_info):
    """Create visualizations based on detected column types"""

    # Time series plot if date column exists
    if col_info['date_cols'] and col_info['numeric_cols']:
        st.subheader("📈 Time Series Analysis")
        date_col = st.selectbox("Select Date Column:", col_info['date_cols'])
        numeric_col = st.selectbox("Select Value Column:", col_info['numeric_cols'])

        if date_col and numeric_col:
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
            df_temp = df_temp.dropna(subset=[date_col, numeric_col])

            if not df_temp.empty:
                daily_data = df_temp.groupby(date_col)[numeric_col].sum().reset_index()
                fig = px.line(daily_data, x=date_col, y=numeric_col, 
                            title=f"{numeric_col} Over Time")
                st.plotly_chart(fig, use_container_width=True)

    # Distribution plots for numeric columns
    if col_info['numeric_cols']:
        st.subheader("📊 Distribution Analysis")
        col1, col2 = st.columns(2)

        with col1:
            num_col = st.selectbox("Select Column for Distribution:", col_info['numeric_cols'])
            if num_col:
                fig = px.histogram(df, x=num_col, title=f"Distribution of {num_col}")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if len(col_info['numeric_cols']) >= 2:
                num_col2 = st.selectbox("Select Second Column:", 
                                      [c for c in col_info['numeric_cols'] if c != num_col])
                if num_col2:
                    fig = px.scatter(df, x=num_col, y=num_col2, 
                                   title=f"{num_col} vs {num_col2}")
                    st.plotly_chart(fig, use_container_width=True)

    # Categorical analysis
    if col_info['categorical_cols']:
        st.subheader("🎯 Categorical Analysis")
        cat_col = st.selectbox("Select Categorical Column:", col_info['categorical_cols'])

        if cat_col:
            # Top categories
            top_categories = df[cat_col].value_counts().head(10)

            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(x=top_categories.index, y=top_categories.values,
                           title=f"Top 10 {cat_col}")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.pie(values=top_categories.values, names=top_categories.index,
                           title=f"{cat_col} Distribution")
                st.plotly_chart(fig, use_container_width=True)

def generate_smart_insights(df, col_info):
    """Generate insights based on data analysis"""
    insights = []

    # Dataset overview
    insights.append(f"📊 **Dataset Overview**: {len(df)} rows × {len(df.columns)} columns")
    insights.append(f"📈 **Numeric Columns**: {len(col_info['numeric_cols'])}")
    insights.append(f"📅 **Date Columns**: {len(col_info['date_cols'])}")
    insights.append(f"🏷️ **Categorical Columns**: {len(col_info['categorical_cols'])}")

    # Missing values analysis
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        top_missing = missing_data[missing_data > 0].head(3)
        insights.append(f"⚠️ **Missing Data**: {top_missing.to_dict()}")

    # Data quality insights
    if col_info['numeric_cols']:
        for col in col_info['numeric_cols'][:3]:  # Top 3 numeric columns
            mean_val = df[col].mean()
            std_val = df[col].std()
            insights.append(f"📊 **{col}**: Mean = {mean_val:.2f}, Std = {std_val:.2f}")

    return insights

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 Universal Data Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload ANY CSV/Excel file and get instant analytics - Works with Kaggle datasets!</p>', 
                unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("📁 Data Upload")

    uploaded_file = st.sidebar.file_uploader(
        "Choose your data file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload any CSV or Excel file - the dashboard will auto-detect columns!"
    )

    # Load sample data option
    use_sample = st.sidebar.checkbox("Use Sample ERP Data", value=not uploaded_file)

    # Load data
    try:
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success(f"✅ Loaded {uploaded_file.name} successfully!")
        elif use_sample:
            df = pd.read_csv('sample_data.csv')
            st.info("📊 Using sample ERP data")
        else:
            st.warning("Please upload a file or use sample data")
            return

    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.info("💡 Make sure your file is a valid CSV or Excel format")
        return

    # Smart column detection
    with st.spinner("🔍 Analyzing your data..."):
        col_info = smart_data_detection(df)

    # Display data info
    st.markdown("## 📋 Data Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Total Rows", f"{len(df):,}")

    with col2:
        st.metric("📋 Total Columns", f"{len(df.columns)}")

    with col3:
        st.metric("🔢 Numeric Columns", f"{len(col_info['numeric_cols'])}")

    with col4:
        st.metric("📅 Date Columns", f"{len(col_info['date_cols'])}")

    # Column type detection results
    st.markdown("### 🎯 Auto-Detected Column Types")

    col1, col2 = st.columns(2)

    with col1:
        if col_info['numeric_cols']:
            st.write("**📊 Numeric Columns:**")
            for col in col_info['numeric_cols']:
                st.write(f"• {col}")

        if col_info['date_cols']:
            st.write("**📅 Date Columns:**")
            for col in col_info['date_cols']:
                st.write(f"• {col}")

    with col2:
        if col_info['categorical_cols']:
            st.write("**🏷️ Categorical Columns:**")
            for col in col_info['categorical_cols']:
                st.write(f"• {col}")

        if col_info['text_cols']:
            st.write("**📝 Text Columns:**")
            for col in col_info['text_cols'][:5]:  # Show first 5
                st.write(f"• {col}")

    # Data filtering
    st.markdown("## 🔧 Data Filters")

    # Row sampling for large datasets
    if len(df) > 10000:
        sample_size = st.slider("Sample Size (for performance)", 1000, len(df), 10000)
        df = df.sample(n=sample_size, random_state=42)
        st.info(f"📊 Using {sample_size} random samples for analysis")

    # Column selection
    selected_columns = st.multiselect(
        "Select Columns for Analysis:",
        options=df.columns.tolist(),
        default=df.columns.tolist()[:10]  # First 10 columns by default
    )

    if selected_columns:
        df_filtered = df[selected_columns]
    else:
        df_filtered = df

    # Smart visualizations
    st.markdown("## 📊 Smart Analytics")

    create_smart_visualizations(df_filtered, 
                               smart_data_detection(df_filtered))

    # Statistical summary
    if col_info['numeric_cols']:
        st.markdown("## 📈 Statistical Summary")
        numeric_df = df_filtered.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            st.dataframe(numeric_df.describe())

    # Correlation matrix
    if len(col_info['numeric_cols']) > 1:
        st.markdown("## 🔗 Correlation Analysis")
        numeric_df = df_filtered.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                          title="Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)

    # Smart insights
    st.markdown("## 🧠 Smart Insights")
    insights = generate_smart_insights(df_filtered, col_info)

    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

    # Raw data view
    st.markdown("## 📋 Data Preview")

    # Show data types
    st.write("**Column Information:**")
    col_types = pd.DataFrame({
        'Column': df_filtered.columns,
        'Data Type': df_filtered.dtypes,
        'Non-Null Count': df_filtered.count(),
        'Null Count': df_filtered.isnull().sum()
    })
    st.dataframe(col_types, use_container_width=True)

    # Data preview
    st.write("**Data Preview:**")
    st.dataframe(df_filtered.head(100), use_container_width=True)

    # Download processed data
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Download Processed Data",
        data=csv,
        file_name="processed_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
