# 📊 Retail Sales Data Analysis & Interactive Dashboard

An end-to-end data analysis project built with Python, Pandas, Plotly, and Streamlit to explore retail sales performance, customer demographics, and product trends through an interactive dashboard.

## 🚀 Project Overview

This project analyzes a retail sales dataset sourced from Kaggle. It uses exploratory data analysis (EDA), business performance metrics, and interactive visualizations to understand sales patterns and customer behavior.

## ✨ Features

- **Key Performance Indicators (KPIs):** Total revenue, transactions, unique customers, units sold, and average transaction value.
- **Interactive Filters:** Filter results by date range, gender, and product category.
- **Product Analysis:** Compare revenue, transaction counts, and units sold across categories.
- **Monthly Sales Trends:** Explore changes in revenue over time.
- **Customer Demographics:** Analyze revenue by gender and age group.
- **Business Insights:** Automatically highlight top-performing categories, months, and gender groups.
- **Transaction Explorer:** Search transaction records by customer ID or product category.
- **CSV Export:** Download filtered transaction data for further analysis.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Jupyter Notebook

## 📁 Project Structure

```text
Retail-Sales-Data-Analysis/
├── data/
│   └── retail_sales_dataset.csv
├── notebooks/
│   └── retail_sales_analysis.ipynb
├── visuals/
├── reports/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 📥 Dataset

Source: [Retail Sales Dataset — Kaggle](https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset)

The dataset contains retail transaction details, including dates, customer IDs, gender, age, product category, quantity, price per unit, and total amount.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Retail-Sales-Data-Analysis
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Add the dataset

Download the CSV from Kaggle and place it here:

```text
data/retail_sales_dataset.csv
```

### 6. Run the dashboard

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 📊 Initial Dataset Findings

The following figures describe the complete dataset used during the initial analysis:

| Metric | Value |
|---|---:|
| Transactions | 1,000 |
| Total revenue | ₹456,000 |
| Units sold | 2,514 |
| Average transaction value | ₹456 |
| Unique customers | 1,000 |

### Initial observations

- Electronics generated ₹156,905 in revenue.
- Clothing recorded the highest transaction count, with 351 transactions.
- Beauty had the highest average transaction value among the three product categories.
- Female customers generated slightly more total revenue than male customers.
- Monthly revenue fluctuated throughout the year.

These are descriptive findings from the dataset, not measures of profit or proof of causal relationships.

## 🎯 Project Objectives

- Practice data cleaning and exploratory data analysis.
- Develop skills in Pandas and data visualization.
- Calculate meaningful retail business KPIs.
- Build an interactive dashboard with Streamlit.
- Communicate findings through data-driven business insights.

## 🔮 Future Improvements

- Add sales forecasting using time-series analysis.
- Add profit and margin analysis when cost data is available.
- Deploy the dashboard online.
- Add automated data-quality checks.
- Improve dashboard styling and add more advanced filters.

## 👨‍💻 Author

**Retail Sales Data Analysis Project**

Developed as a practical data science and analytics project using Python.

## 📄 Disclaimer

This project is intended for educational and portfolio purposes. Business insights are based on the supplied dataset and should not be interpreted as financial or causal conclusions.
