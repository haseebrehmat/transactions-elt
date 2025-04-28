# 05 - The Dashboard (The Presentation)

Data isn't useful until people can see it. We built a dashboard using **Streamlit**, which is a library that lets you build web apps using only Python.

## How it works
The dashboard connects to **MinIO** (our storage) and searches for folders in the `pipeline-runs` bucket. 

### Features of our Dashboard:

### 1. Run Selector
In the sidebar, you can pick which "Run" you want to look at. Since we save a snapshot of every step, you can look at yesterday's results or just the latest one.

### 2. The Tabs (Step-by-Step)
We have a tab for every stage of the pipeline. This is great for debugging!
- If the "Success Only" tab looks empty, but the "Cleaned" tab has data, you know exactly where the problem is.

### 3. Final Analytics
In the "Daily Aggregation" tab, we show:
- **Big Metrics**: High-level numbers like "Total Volume Processed."
- **Trend Charts**: A visual look at transaction amounts over time.
- **Top Customers**: A bar chart showing who is moving the most money.

## Why Streamlit?
It's incredibly fast to build. We don't need to learn HTML, CSS, or JavaScript. We just write:
```python
st.title("My Dashboard")
st.bar_chart(my_dataframe)
```
...and it creates a beautiful, interactive web page!

---
**Next Step:** [Advanced Deep Dive & Iceberg](06_advanced_iceberg.md)
