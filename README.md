# 📊 Retail Sales Data Analysis & Interactive Dashboard

An end-to-end data analytics project that explores retail sales data, identifies customer purchasing patterns, and presents business insights through an interactive dashboard built with Python and Streamlit.

## 📌 Project Overview

Understanding sales performance and customer behavior helps businesses make better decisions. This project analyzes retail transaction data to discover which product categories generate the most revenue, how sales change over time, and how purchasing patterns differ across customer groups.

The project combines **Exploratory Data Analysis (EDA), data visualization, and an interactive dashboard** to turn raw sales data into meaningful business insights.

## 🎯 Project Objectives

- Analyze overall retail sales performance.
- Identify the highest-revenue product categories.
- Understand monthly sales trends.
- Compare purchasing patterns by gender.
- Analyze customer age groups and spending behavior.
- Build an interactive dashboard with filters.
- Help users explore transactions and download filtered data.

## ✨ Key Features

- **Interactive dashboard:** Explore sales data through an easy-to-use interface.
- **Sales KPI cards:** View total revenue, transactions, unique customers, units sold, and average transaction value.
- **Category analysis:** Compare revenue and sales performance across product categories.
- **Monthly sales trends:** Track revenue over time.
- **Customer analysis:** Compare sales by gender and age group.
- **Sidebar filters:** Filter results by date range, gender, and product category.
- **Transaction explorer:** Search and inspect individual transactions.
- **CSV export:** Download filtered transaction data for further analysis.
- **Business insights:** Display useful observations based on the selected data.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data cleaning, manipulation, and analysis |
| NumPy | Numerical operations |
| Plotly | Interactive charts and visualizations |
| Streamlit | Interactive web dashboard |
| Jupyter Notebook | Exploratory data analysis |
| Git and GitHub | Version control and project hosting |

## 📂 Project Structure

```text
Retail-Sales-Data-Analysis/
│
├── app.py                         # Main Streamlit dashboard
├── requirements.txt               # Required Python libraries
├── README.md                      # Project documentation
├── .gitignore                     # Files excluded from Git
├── streamlit_config.toml          # Streamlit configuration
│
├── assets/
│   └── background.jpg              # Dashboard background asset
│
├── data/
│   └── retail_sales_dataset.csv    # Retail sales dataset
│
└── notebooks/
    └── retail_sales_analysis.ipynb # Exploratory data analysis
```

## 📊 Dataset Information

**Dataset:** Retail Sales Dataset

**Source:** [Download/View dataset on Kaggle](https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset)

The dataset contains **1,000 transactions and 9 columns** describing retail purchases.

| Column | Description |
|---|---|
| Transaction ID | Unique transaction identifier |
| Date | Date of purchase |
| Customer ID | Customer identifier |
| Gender | Customer gender |
| Age | Customer age |
| Product Category | Category of the purchased product |
| Quantity | Number of units purchased |
| Price per Unit | Price of one unit |
| Total Amount | Total transaction amount |

## 🔍 Exploratory Data Analysis

The Jupyter Notebook explores the dataset through the following steps:

1. Load the dataset using Pandas.
2. Inspect rows, columns, and data types.
3. Check for missing values and duplicate records.
4. Calculate descriptive statistics.
5. Analyze revenue and transaction metrics.
6. Compare product categories and customer groups.
7. Visualize monthly sales trends and purchasing behavior.
8. Summarize key findings.

## 📈 Key Findings

Based on the current analysis of the dataset:

- **Total revenue:** ₹456,000
- **Total transactions:** 1,000
- **Unique customers:** 1,000
- **Total units sold:** 2,514
- **Average transaction value:** ₹456
- **Highest-revenue category:** Electronics, with ₹156,905.
- **Lowest-revenue category:** Beauty, with ₹143,515.
- **Highest-revenue month:** May, with ₹53,150.
- **Lowest-revenue month:** September, with ₹23,620.
- **Gender comparison:** Female customers contributed ₹232,840 in revenue, while male customers contributed ₹223,160.

These findings describe the supplied dataset and are not necessarily representative of all retail businesses. Results shown in the dashboard may change when filters are applied.

## 🚀 Getting Started

Follow these instructions to download and run the project on your computer.

### Prerequisites

Install the following software:

- [Python](https://www.python.org/downloads/) — preferably Python 3.11 or newer.
- [Git](https://git-scm.com/downloads) — to clone the repository.
- A code editor such as [Visual Studio Code](https://code.visualstudio.com/).

### Step 1: Clone the repository

Open PowerShell, Command Prompt, or a terminal and run:

```bash
git clone https://github.com/shailesh-23-patil/Retail-Sales-Data-Analysis.git
```

### Step 2: Open the project folder

```bash
cd Retail-Sales-Data-Analysis
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this command in the same terminal and then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

### Step 5: Install the required libraries

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Verify the dataset

Make sure the following file exists:

```text
data/retail_sales_dataset.csv
```

The dataset is included in this repository. If it is missing, download it from the Kaggle link above and place it in the `data` folder using the exact filename.

### Step 7: Run the dashboard

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser to use the dashboard.

To stop the dashboard, press `Ctrl + C` in the terminal.

## 🖥️ How to Use the Dashboard

1. Start the application using the command above.
2. Review the KPI cards to understand overall sales performance.
3. Use the sidebar to select a date range, gender, or product category.
4. Explore category revenue, monthly trends, gender comparisons, and age-group charts.
5. Read the automatically generated business insights.
6. Search the transaction explorer to inspect individual records.
7. Use the CSV download option to export the filtered transactions.

The charts and summary metrics respond to the selected filters.

## 💡 Business Applications

This type of analysis can help retail teams:

- Identify high-performing product categories.
- Understand changes in monthly revenue.
- Compare customer purchasing patterns.
- Explore transaction-level sales data.
- Support decisions about marketing, promotions, and inventory planning.

The project demonstrates analytical methods; it does not independently prove the causes of sales changes or forecast future revenue.

## 🔮 Future Improvements

Potential enhancements include:

- Add sales forecasting using machine learning.
- Include profit and profit-margin analysis if cost data becomes available.
- Add customer segmentation and purchasing frequency analysis.
- Compare sales across stores or regions if location data is available.
- Deploy the dashboard online for public access.
- Add automated data-quality checks and more advanced filters.

## 👨‍💻 Author

**Shailesh Patil**

- GitHub: [shailesh-23-patil](https://github.com/shailesh-23-patil)
- Project repository: [Retail-Sales-Data-Analysis](https://github.com/shailesh-23-patil/Retail-Sales-Data-Analysis)

## 📄 License

No license has currently been specified. Unless a license is added, others should not assume they have permission to redistribute or reuse this project's code.

---

⭐ If you find this project useful for learning data analysis and visualization, consider giving the repository a star on GitHub.
