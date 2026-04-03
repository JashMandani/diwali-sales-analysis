# 🪔 Diwali Sales Analysis

> A comprehensive Exploratory Data Analysis (EDA) project on Diwali festive season sales data — uncovering customer behavior across demographics, geographies, and product categories to drive smarter marketing decisions.

---

## 📌 Project Overview

| Detail | Info |
|--------|------|
| **Domain** | Retail / E-Commerce |
| **Type** | Exploratory Data Analysis (EDA) |
| **Dataset** | 11,239 records, 13 features |
| **Tools** | Python, Pandas, Matplotlib, Seaborn, ReportLab |
| **Output** | Charts + PDF Report |

---

## 🎯 Problem Statement

Analyze Diwali sales data to identify customer purchasing behavior across demographics (age, gender, marital status, occupation, and region) and product categories. The goal is to discover key patterns that help:

- Optimize marketing strategies
- Improve customer targeting
- Maximize sales revenue during festive seasons

---

## 📁 Project Structure

```
diwali_sales_analysis/
│
├── data/
│   └── Diwali_Sales_Data.csv          # Raw dataset
│
├── notebooks/
│   └── diwali_eda.ipynb               # Full EDA Jupyter Notebook
│
├── scripts/
│   ├── data_cleaning.py               # Data loading & preprocessing
│   ├── eda_analysis.py                # All EDA & visualizations
│   └── generate_report.py             # PDF report generation
│
├── charts/                            # All generated chart PNGs
├── outputs/
│   └── Diwali_Sales_Report.pdf        # Final PDF report
│
├── requirements.txt                   # Python dependencies
└── README.md
```

---

## 📊 Dataset Description

| Column | Description |
|--------|-------------|
| `User_ID` | Unique customer identifier |
| `Cust_name` | Customer name |
| `Product_ID` | Unique product identifier |
| `Gender` | M / F |
| `Age Group` | Age bracket (0-17, 18-25, 26-35, etc.) |
| `Age` | Exact age |
| `Marital_Status` | 0 = Single, 1 = Married |
| `State` | State of purchase |
| `Zone` | Region (Western, Southern, Central, Northern, Eastern) |
| `Occupation` | Customer's profession |
| `Product_Category` | Category of purchased product |
| `Orders` | Number of orders |
| `Amount` | Total purchase amount (₹) |

---

## 🔍 Key Findings

### 👥 Gender
- **Female** buyers drive ~65% of total revenue
- Women place more orders with higher purchase frequency

### 🎂 Age Group
- **26–35** is the highest-spending age group
- **36–45** is a strong second — established households with buying power

### 🗺️ Geography
- **Maharashtra** leads all states in revenue
- **Western Zone** is the top-performing region

### 💼 Occupation
- **IT Sector** and **Healthcare** professionals are top spenders
- Agriculture & Textile sectors are the most price-sensitive

### 🛒 Product Categories
- **Clothing & Apparel**, **Food**, and **Electronics** are top performers
- Pet Care & Veterinary are niche growth segments

### 💍 Marital Status
- **Married women aged 26–35** are the single highest-value customer segment

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/diwali-sales-analysis.git
cd diwali-sales-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the analysis

**Option A — Run all scripts:**
```bash
python scripts/data_cleaning.py
python scripts/eda_analysis.py
python scripts/generate_report.py
```

**Option B — Jupyter Notebook:**
```bash
jupyter notebook notebooks/diwali_eda.ipynb
```

---

## 📈 Visualizations

| Chart | Description |
|-------|-------------|
| Gender Distribution | Revenue & orders split by gender (pie) |
| Age Group Revenue | Bar chart of revenue per age group |
| Top 10 States | Horizontal bar chart of state-wise revenue |
| Zone Analysis | Revenue & orders by zone |
| Occupation Revenue | Revenue by occupation type |
| Product Categories | Top 10 categories by revenue |
| Marital Status × Gender | Grouped bar by status and gender |

---

## 🎯 Strategic Recommendations

1. **Primary Target**: Married women aged 26–35 in IT/Healthcare in Western India
2. **Geography**: Focus on Maharashtra, Uttar Pradesh, Karnataka
3. **Product Priority**: Lead with Clothing, Food, and Electronics
4. **Channels**: Instagram & WhatsApp for female demo; LinkedIn for IT/Banking
5. **Loyalty Programs**: Build repeat-purchase incentives for 36–45 age group
6. **Regional Expansion**: Run growth campaigns in the under-penetrated Eastern zone

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Pandas** — data manipulation
- **Matplotlib / Seaborn** — visualizations
- **ReportLab** — PDF generation
- **Jupyter** — interactive notebook

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋 Author

**Your Name**  
[GitHub](https://github.com/yourusername) • [LinkedIn](https://linkedin.com/in/yourprofile)

---

*Made with 🪔 and Python*
