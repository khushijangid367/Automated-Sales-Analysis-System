# 📊 Automated Sales Analysis System
### Python · SQLite · Tableau · Scikit-learn

> **Business Question:** *Which customer segment and region combination is most profitable — and are discounts actually growing revenue or silently destroying margins?*

---

## 🔍 Key Findings

| Finding | Detail |
|---|---|
| 💀 Discount Killer | Orders with **50% discount** generate **negative profit margins** on average |
| ✅ Sweet Spot | **0–10% discount** orders sustain **40–45% profit margins** |
| 🏆 Top Segment | **Home Office (North)** and **Consumer** segments show highest margin % |
| 🎯 ML Segments | K-Means identified 3 distinct customer types: **High Value**, **Regular**, **Margin Killers** |

---

## 🖼️ Dashboard Preview

> [📌 *Add your Tableau Public link here once published*](https://public.tableau.com/app/profile/khushi.jangid1214/viz/Automated-Sales-Analysis-System-Dashboard/Dashboard1?publish=yes)

<img width="1599" height="769" alt="image" src="https://github.com/user-attachments/assets/723171ff-b1c9-49df-b98b-d39d85d4a506" />

**Customer Segmentation (K-Means)**

<img width="1600" height="792" alt="WhatsApp Image 2026-05-03 at 12 35 37 AM" src="https://github.com/user-attachments/assets/90fe754f-296b-4aee-a345-af2b3f2d222b" />


---

## 🏗️ Project Architecture

```
SALES-ANALYSIS-PROJECT/
│
├── data/
│   ├── raw_sales.csv          ← Kaggle Superstore dataset (raw)
│   └── cleaned_data.csv       ← Output of cleaning.py
│
├── scripts/
│   ├── cleaning.py            ← Production-grade data cleaning pipeline
│   ├── setup_sql.py           ← Loads cleaned data into SQLite
│   ├── analysis.py            ← SQL aggregations via Python
│   ├── segmentation.py        ← K-Means customer clustering (ML)
│   └── queries.sql            ← Raw SQL queries reference file
│
├── notebooks/
│   └── eda_visuals.py         ← EDA scatter plots and visual exploration
│
├── outputs/
│   ├── segment_profitability.csv
│   ├── discount_impact.csv
│   ├── customer_clusters.png
│   └── profit_loss_scatter.png
│
├── app/                       ← Streamlit app (coming soon)
├── sales_data.db              ← SQLite database
└── automate.py                ← Master pipeline orchestrator
```

---

## ⚙️ Pipeline Flow

```
raw_sales.csv
      │
      ▼
 cleaning.py        → Standardizes columns, parses dates, scrubs currency,
                       caps outliers, engineers Profit & Profit_Margin
      │
      ▼
 setup_sql.py       → Loads cleaned_data.csv into SQLite (sales_data.db)
      │
      ▼
 analysis.py        → SQL GROUP BY queries: segment profitability,
                       discount impact → exports to /outputs
      │
      ▼
 segmentation.py    → K-Means (k=3) with StandardScaler on Revenue +
                       Profit_Margin → dynamic cluster labeling → PNG export
```

**Run the entire pipeline with one command:**
```bash
python automate.py
```

---

## 🛠️ Tech Stack

| Layer | Tools Used |
|---|---|
| Data Cleaning | Python, Pandas, NumPy |
| Database & Querying | SQLite, SQL (GROUP BY, aggregations, CTEs) |
| Machine Learning | Scikit-learn (KMeans, StandardScaler) |
| Visualization | Matplotlib, Seaborn, Tableau |
| Automation | Python subprocess, os, sys |

---

## 🐛 Real-World Bugs Resolved

These are actual errors encountered and fixed during development — not a tutorial run-through:

| Error | Root Cause | Fix Applied |
|---|---|---|
| `UnicodeDecodeError` | Kaggle CSV had special characters | Switched `pd.read_csv` encoding to `latin1` |
| `TypeError` on math ops | Financial columns imported as strings (contained `$`, `,`) | Wrote custom scrubber to strip symbols → `pd.to_numeric` |
| `KeyError: 'customer_id'` | Kaggle uses `customer_name`, not `customer_id` | Debugged with `df.columns.tolist()`, updated script |
| `FileNotFoundError` | Relative paths broke when running from different directories | Upgraded all paths to absolute using `os.path.abspath(__file__)` |
| `PermissionError` | CSV was open in Excel (Windows file lock) | Closed Excel before running script |

---

## 📈 ML Segmentation — How It Works

The K-Means model clusters customers along two axes:
- **Revenue** (total order value)
- **Profit_Margin** (profitability ratio)

Data is standardized with `StandardScaler` before clustering so large revenue values don't dominate the margin signal.

Cluster labels are **dynamically assigned** — not hardcoded. After fitting, centroids are ranked by mean profit, and labels (`High Value`, `Regular`, `Margin Killers`) are mapped programmatically. This means the script adapts correctly to any new dataset.

---

## 🚀 How to Run

**1. Clone the repo**
```bash
git clone https://github.com/khushijangid367/sales-analysis-project
cd sales-analysis-project
```

**2. Install dependencies**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

**3. Add the dataset**

Download the [Kaggle Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) and place it at:
```
data/raw_sales.csv
```

**4. Run the full pipeline**
```bash
python automate.py
```

Outputs will appear in the `/outputs` folder.

---

## 📂 Dataset

**Source:** [Sample Superstore — Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

A widely-used retail dataset containing order-level sales data across customer segments, regions, product categories, and discount tiers.

---

## 👩‍💻 Author

**Khushi Jangid**
B.Tech CSE · Government Engineering College, Ajmer
Minor Degree in CSE · IIT Mandi

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/khushi-jangid-2454b3341/)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black)](https://github.com/khushijangid367)
# Automated-Sales-Analysis-System
