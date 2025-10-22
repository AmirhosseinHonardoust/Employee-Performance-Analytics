# Employee Performance Analytics (SQL + Python)

Analyze employee performance and departmental productivity using **SQL (SQLite)** for KPI aggregation and **Python** for analytics and visualization.  
This project transforms HR data into **actionable business insights**, identifying high performers, efficiency trends, and departmental KPIs.

---

## Overview

This project demonstrates how to:
- Use **SQL** for feature engineering and KPI calculation
- Use **Python** for data analysis and visualization
- Deliver **data-driven HR insights** in an end-to-end workflow

---

## Objectives

- Compute **department-level performance indicators**
- Assess **employee efficiency and attendance**
- Visualize **relationships between workload, tasks, and ratings**
- Generate clean and ready-to-use summary reports

---

## Project Structure

```
employee-performance-analytics/
├── README.md
├── requirements.txt
├── data/
│   └── employees.csv
├── src/
│   ├── create_db.py
│   ├── queries.sql
│   ├── analyze_performance.py
│   └── utils.py
└── outputs/
    ├── department_kpis.csv
    ├── performance_summary.csv
    └── charts/
        ├── avg_rating_by_department.png
        ├── performance_vs_hours.png
        └── task_completion_rate.png
```

---

## Dataset Description

| Column | Description |
|---------|-------------|
| `employee_id` | Unique employee identifier |
| `name` | Employee name |
| `department` | Department name (Engineering, Sales, etc.) |
| `role` | Role title |
| `date` | Record date (YYYY-MM-DD) |
| `tasks_completed` | Number of tasks completed |
| `hours_worked` | Hours worked on that day |
| `rating` | Daily performance rating (1–5) |
| `projects` | Active projects |
| `absences` | 1 if absent, else 0 |

> The dataset (`employees.csv`) is synthetic, generated with realistic departmental trends and biases.

---

## SQL Logic: `src/queries.sql`

The SQL script creates views and extracts three analytical datasets:

1. **`department_kpis`** – Department-level KPIs:
   - Average rating
   - Tasks per department
   - Total hours
   - Absence rates

2. **`employee_summary`** – Individual performance summaries:
   - Total tasks, hours, projects, absences
   - Average ratings
   - Tasks per hour (efficiency)

3. **`daily_productivity`** – Day-wise workload and productivity data.

---

## Visualizations

### Average Rating by Department
**Chart:** `outputs/charts/avg_rating_by_department.png`

<img width="1200" height="750" alt="avg_rating_by_department" src="https://github.com/user-attachments/assets/6b5666ae-d7ed-4a56-948b-2944122a24e0" />

**Insight:**
- Clear variation between departments (Finance & Engineering higher, Support & Sales lower)
- Indicates which departments maintain strong consistency and performance culture.

---

### Performance vs Hours Worked
**Chart:** `outputs/charts/performance_vs_hours.png`

<img width="1200" height="750" alt="performance_vs_hours" src="https://github.com/user-attachments/assets/b894b553-2adc-4373-9583-f531b10efbbe" />

**Insight:**
- Positive correlation: higher hours → more tasks (up to a plateau)
- Clusters show standard workloads; outliers can reveal inefficiency or exceptional performers.

---

### Task Completion Rate Distribution
**Chart:** `outputs/charts/task_completion_rate.png`

<img width="1200" height="750" alt="task_completion_rate" src="https://github.com/user-attachments/assets/a4f5dd3b-4179-49e6-a921-6bc75a8083d7" />

**Insight:**
- Most employees average around **1 task/hour**
- High performers exceed 1.4, low performers under 0.8
- Useful for spotting training needs or recognizing excellence.

---

## Getting Started

### Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Load Data into SQLite
```bash
python src/create_db.py --csv data/employees.csv --db hr.db
```

### Run Analysis
```bash
python src/analyze_performance.py --db hr.db --sql src/queries.sql --outdir outputs
```

All CSV reports and charts will be saved in the `outputs/` directory.

---

## Key Insights

- **Department-level performance gaps** can reveal resource or leadership factors.
- **Efficiency distribution** (tasks/hour) identifies both low performers and power users.
- **Workload-to-performance trends** help balance effort vs productivity.
- **Absence tracking** adds HR alignment to the analysis.

---

## Tools Used

| Tool | Purpose |
|------|----------|
| **Python (pandas, matplotlib)** | Data manipulation & visualization |
| **SQLite** | Querying & KPI computation |
| **SQL** | Feature engineering & aggregation |
| **Jupyter / VS Code** | Development & presentation |

---

## Project Value

This project demonstrates:
- **SQL + Python integration** for analytics
- **Data storytelling and visualization**
- **Human Resource analytics capability**
- Clean, modular, and reproducible data science workflow
