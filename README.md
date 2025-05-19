# PyAnalyzer
A Python tool for analyzing CSV files and generating Power BI-like dashboards with summaries and visualizations.

## Features
- Load and analyze CSV files
- Generate dataset summaries (shape, columns, data types, missing values, stats)
- Create interactive visualizations (bar charts, pie charts, histograms)
- Explore data with sorting and filtering in a web-based dashboard

## Requirements
- Python 3.8+ (due to Streamlit compatibility)
- Libraries: `pandas`, `matplotlib`, `seaborn`, `streamlit`

## Setup
1. Create a `PyAnalyzer` folder and place `app.py`, `requirements.txt`, and this `README.md` inside.
2. Create a `data/` folder and add your CSV files (e.g., `sample_data.csv`).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install streamlit pandas matplotlib seaborn
## How to Run
1.Navigate to the project directory.
2.Run the following command:
```bash
 streamlit run app.py
