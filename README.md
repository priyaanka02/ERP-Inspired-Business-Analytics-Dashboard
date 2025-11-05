# 🏢 ERP-Inspired Business Analytics Dashboard

> **Streamlit dashboard processing 10,000+ sales records with automated KPIs, SAP-style reporting, and real-time business insights** 📊✨

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.49.0-red)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Records](https://img.shields.io/badge/Records-10K%2B-orange)

## 🎯 Project Overview

This **ERP-inspired analytics dashboard** transforms business data into actionable insights with **SAP-style reporting**. Built with Streamlit and featuring intelligent data processing, it delivers automated KPIs, revenue decline alerts, and customer churn predictions—all through an interactive, mobile-responsive interface.

Perfect for business analysts who need quick, reliable insights from sales data! 🚀

---

## ✨ Key Features

### 📊 **Automated KPI Generation**
- **Real-time metrics**: Revenue, growth %, average order value, customer count
- **Monthly growth tracking**: Automatic calculation of month-over-month changes
- **Data quality scoring**: Instant assessment of dataset completeness
- **SAP-style KPI cards**: Professional dashboard layout with color-coded indicators

### 🚨 **Revenue Decline Alerts**
- **Intelligent alert system**: Detects significant revenue declines (>10%)
- **Severity classification**: High/Medium priority based on decline magnitude  
- **Trend analysis**: Identifies negative patterns across 3+ months
- **Actionable insights**: Current vs. previous period comparisons

### 🎯 **Customer Churn Prediction**
- **Rule-based prediction engine**: No ML libraries, pure logic-driven analysis
- **Risk scoring (0-100)**: Considers recency, frequency, and monetary value
- **Risk categorization**: High/Medium/Low risk segments
- **Top at-risk identification**: Automatically flags customers needing attention

### 📈 **Interactive Visualizations (Plotly)**
- **Time series analysis**: Revenue trends, sales patterns over time
- **Distribution charts**: Histograms with statistical overlays
- **Correlation analysis**: Scatter plots with trend lines
- **Category breakdowns**: Top 10 rankings with color-coded bars
- **Real-time charts**: Dynamic updates with data changes

### 💼 **ERP-Style Reporting**
- **Professional design**: SAP-inspired color scheme and layout
- **Mobile-responsive**: Adapts to all screen sizes
- **Session persistence**: Data stays loaded during active session
- **Export functionality**: Download processed data as CSV

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit (web interface) |
| **Data Processing** | Pandas, NumPy |
| **Visualizations** | Plotly Express & Graph Objects |
| **Business Logic** | Custom Python analytics engine |
| **Styling** | Custom CSS (SAP-inspired) |

---

## 🚀 Quick Start

### 1️⃣ **Clone the Repository**
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Run the Dashboard**
```bash
streamlit run app.py
```

### 4️⃣ **Access the App**
Open your browser to `http://localhost:8501`

### 5️⃣ **Upload Data or Use Demo**
- Upload your CSV/Excel file via sidebar
- Or check "Use Demo Data" for instant preview

---

## 📁 Project Structure

```
erp-business-dashboard/
├── app.py                 # Main Streamlit application
├── utils.py               # Business logic & analytics functions
├── sample_data.csv        # Demo dataset (10,000+ records)
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

---

## 📊 What It Actually Does

### **Automated KPI Dashboard**
Instantly calculates and displays:
- 💰 Total Revenue
- 📈 Monthly Growth %
- 📦 Total Orders
- 👥 Unique Customers
- 💵 Average Order Value
- 🔍 Data Quality Score

### **Revenue Decline Detection**
Monitors business health by:
- Comparing current vs. previous month revenue
- Detecting declines > 10% (configurable threshold)
- Analysing 3-month trends for negative patterns
- Generating actionable alerts with severity levels

### **Churn Risk Prediction**
Identifies at-risk customers using:
- **Recency**: Days since last purchase (40 points max)
- **Frequency**: Order count analysis (30 points max)  
- **Monetary**: Revenue value relative to average (30 points max)
- **Output**: Risk score (0-100) + High/Medium/Low category

### **Data Visualizations**
Creates interactive charts:
- **Time Series**: Daily/monthly revenue trends
- **Distributions**: Histograms with box plots
- **Correlations**: Scatter plots with trend lines
- **Categories**: Top 10 rankings by any metric

---

## 📈 Sample Dataset

Included `sample_data.csv` features:
- **10,000+ sales records** (expandable to 100K+)
- **Date range**: Jan 2023 - Aug 2023
- **Columns**: OrderID, Date, Customer, Product, Quantity, Price, Total_Sales
- **8 B2B customers**: TechCorp Inc, Innovation Hub, etc.
- **8 product categories**: Laptops, Smartphones, Tablets, Monitors, Headphones, Keyboards, Mice, Speakers

Perfect for testing all dashboard features! 🎉

---

## 🎨 Design Philosophy

### **SAP-Inspired Interface**
- Professional blue colour scheme (`#0070F2`)
- Clean, card-based layout
- High-contrast alerts (red/orange/green)
- Mobile-first responsive design

### **Real-Time Insights**
- Live status indicator with pulse animation
- Session state management for data persistence
- Instant metric recalculation on data upload
- Dynamic chart updates

### **User-Friendly**
- Zero configuration required
- Automatic column detection (dates, numbers, categories)
- Clear help text and tooltips
- One-click data export

---

## 💡 Key Technical Features

### **Smart Data Detection**
```python
# Automatically identifies:
- Numeric columns (for calculations)
- Date columns (for time series)
- Categorical columns (for grouping)
- Text columns (for labels)
```

### **Business Analytics Engine**
```python
# Core functions:
- calculate_monthly_growth()
- detect_revenue_decline_alerts()
- predict_churn_risk()
- analyze_product_dependency()
- generate_kpi_summary()
```

### **Session State Management**
```python
# Persistent data storage:
- Uploaded dataset cached
- Last upload timestamp tracked
- No data loss during interactions
```

---

## 🎯 Use Cases

✅ **Business Analysts**: Quick revenue and customer insights  
✅ **Sales Teams**: Monitor performance and identify at-risk accounts  
✅ **Data Professionals**: Portfolio demonstration of Streamlit + analytics  
✅ **Students**: Learn business intelligence and data visualization   

---

## 🚀 Scalability

### **Current Capabilities**
- ✅ Handles 10,000+ records smoothly
- ✅ CSV and Excel file support
- ✅ Mobile-responsive design
- ✅ Session-based data persistence

### **Performance Optimizations**
- Efficient pandas operations
- Strategic data sampling for large datasets
- Plotly's built-in optimization
- Streamlit caching for repeated operations

---

## 📝 Future Enhancements

Potential additions (not currently implemented):
- 🔮 Machine learning forecasting (Prophet/ARIMA)
- 🗄️ Database connectivity (PostgreSQL/MySQL)
- 📄 PDF report generation
- 🔐 User authentication
- 🌐 API data ingestion
- 📊 Advanced cohort analysis

---

## 🎓 Skills Demonstrated

This project showcases:
- ✅ **Python programming** (Pandas, NumPy)
- ✅ **Web development** (Streamlit)
- ✅ **Data visualization** (Plotly)
- ✅ **Business analytics** (KPIs, metrics, churn)
- ✅ **Algorithm design** (prediction logic)
- ✅ **UI/UX design** (responsive CSS)
- ✅ **Problem-solving** (alert systems, data quality)

---

## 📦 Dependencies

```txt
streamlit>=1.49.0
pandas>=2.3.2
numpy>=1.24.0
plotly>=5.24.1
openpyxl>=3.1.5
```

---

## 🤝 Contributing

This is a portfolio/interview project, but suggestions are welcome!

---

