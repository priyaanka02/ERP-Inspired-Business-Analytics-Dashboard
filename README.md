# 📊 ERP-Inspired Business Analytics Dashboard

> A comprehensive Streamlit-based business intelligence platform for data analysis and visualization, built with automated insights and real-time analytics capabilities.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.49%2B-red) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🚀 Project Overview

This business analytics dashboard provides an intelligent, automated approach to analyzing business data with features inspired by enterprise ERP systems. The platform automatically detects data structures, generates key performance indicators (KPIs), and delivers actionable insights through interactive visualizations.

### ✨ Key Features

- **🔍 Smart Data Detection**: Automatically recognizes column types and business data patterns
- **📈 Real-time KPI Generation**: Automated calculation of revenue, growth, and customer metrics
- **⚠️ Business Alerts**: Revenue decline detection and trend analysis
- **👥 Customer Analytics**: Churn prediction and risk scoring algorithms
- **🎯 Product Intelligence**: Revenue concentration and dependency analysis
- **📱 Mobile-Responsive Design**: SAP-inspired UI that works on all devices
- **💾 Session Persistence**: Data remains loaded throughout your analysis session
- **🔄 Multi-format Support**: Handles CSV, Excel (.xlsx, .xls) files up to 100K records

## 🛠️ Technical Stack

- **Frontend**: Streamlit with custom CSS
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly (Interactive charts and graphs)
- **Analytics Engine**: Custom business intelligence algorithms
- **File Handling**: Support for CSV and Excel formats

## 📋 Prerequisites

- Python 3.8 or higher
- 50MB+ available memory for large datasets
- Web browser (Chrome, Firefox, Safari, Edge)

## ⚡ Installation & Setup

1. **Clone the repository**
git clone [your-repository-url]
cd erp-business-analytics


2. **Install dependencies**
pip install -r requirements.txt


3. **Run the application**
streamlit run app.py


4. **Access the dashboard**
   - Open your browser to `http://localhost:8501`
   - Upload your data file or use the demo dataset

## 📊 Data Requirements

### Recommended Column Types
- **Date fields**: `order_date`, `transaction_date`, `created_at`, etc.
- **Customer data**: `customer_name`, `customer_id`, `client`, etc.
- **Product info**: `product_name`, `item`, `sku`, `category`, etc.
- **Financial data**: `total_sales`, `revenue`, `amount`, `price`, etc.
- **Quantity fields**: `quantity`, `units_sold`, `count`, etc.

### Supported File Formats
- CSV files (UTF-8 encoded)
- Excel files (.xlsx, .xls)
- Maximum recommended size: 100K rows

## 🎯 Core Analytics Features

### 1. **Automated KPI Dashboard**
- Total Revenue with currency detection (₹, $, €, £, ¥)
- Monthly Growth Rate calculation
- Customer count and order volume
- Data quality scoring

### 2. **Revenue Analytics**
- Month-over-month growth tracking
- Revenue decline alerts with severity levels
- Trend analysis and forecasting indicators

### 3. **Customer Intelligence**
- Churn risk scoring (High/Medium/Low categories)
- Customer lifetime value analysis
- Purchase behavior patterns
- At-risk customer identification

### 4. **Product Performance**
- Revenue concentration analysis
- Top-performing product identification
- Product dependency metrics
- Category-wise performance breakdown

### 5. **Interactive Visualizations**
- Time series analysis charts
- Statistical distributions
- Correlation matrices and scatter plots
- Category performance comparisons

## 🔧 Advanced Capabilities

### Smart Column Mapping
The system automatically detects and maps common business column names:
Examples of auto-detected columns
Date: order_date, transaction_date, created_at
Customer: customer_name, client_id, buyer
Product: product_name, item, sku
Sales: total_sales, revenue, amount

### Currency Support
- Automatic currency symbol detection
- Multi-currency formatting (Dollar, Euro, Rupee, Pound, Yen)
- Large number formatting with K/M/B suffixes

### Business Alerts System
- Revenue decline notifications
- Negative trend warnings
- Configurable threshold settings
- Severity-based color coding

## 📈 Usage Examples

### Basic Analysis Flow
1. Upload your business data file
2. Review auto-detected column mappings
3. Explore generated KPIs on the main dashboard
4. Check revenue alerts and warnings
5. Analyze customer churn predictions
6. Examine interactive visualizations
7. Download processed data for further use

### Demo Mode
Use the built-in demo dataset to explore features:
- ✅ Check "Use Demo Data" in the sidebar
- 🔍 Explore 10,000+ sample records
- 📊 See all features in action

## 🎨 UI/UX Features

- **SAP-Style Design**: Professional enterprise interface
- **Color-coded Alerts**: Immediate visual feedback
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live status indicators
- **Intuitive Navigation**: Tab-based organization

## 🔍 File Structure

├── app.py # Main Streamlit application
├── utils.py # Business analytics utilities
├── requirements.txt # Python dependencies
├── sample_data.csv # Demo dataset (2.3M+ records)
└── README.md # Project documentation


## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional visualization types
- Advanced machine learning models
- Real-time data streaming integration
- Export functionality improvements



---

**Made with ❤️ for business intelligence and data-driven decision making**

*Last updated: November 2025*
This is a portfolio/interview project, but suggestions are welcome!

---

