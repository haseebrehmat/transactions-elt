# 12 - Code Deep Dive: Analytics Dashboard (`app.py`)

Our dashboard uses **Streamlit** to provide a real-time window into our data lake.

---

## **1. UI & Visual Identity**
The script starts with `st.set_page_config` and a large block of `st.markdown` containing **CSS**.
- **Dark Theme**: We manually override styles to create a professional "Bank Sentinel" dark aesthetic.
- **Custom Metrics**: We styled the `[data-testid="stMetricValue"]` to ensure numbers "pop" in emerald green.

---

## **2. Connection Backend**
### **`get_s3_client()`**
- Uses **Caching**: `@st.cache_resource` ensures we don't reconnect to MinIO every time a user clicks a button. One connection is shared.

### **`list_runs()`**
- **Action**: Queries the `pipeline-runs` bucket and looks for "folders" (CommonPrefixes).
- **Result**: populates the dropdown in the sidebar.

### **`load_data(run_folder, stage_name)`**
- This is the core data-fetcher.
1. It looks into a specific run's folder.
2. It finds the `.csv` file.
3. It uses `pd.read_csv(io.BytesIO(...))` to read the data file directly from the "Cloud" memory into a Pandas DataFrame.

---

## **3. The Multi-Stage Tabs**
We loop through our defined `STAGES` dictionary and create a `st.tabs()` interface.

### **Generic Stage View**
- For stages 1 through 5, we simply show the first 100 rows using `st.dataframe()`.
- We add a "Status Distribution" bar chart to show the mix of SUCCESS, FAILED, and PENDING transactions.

### **Final Aggregation View (`6_daily_aggregation`)**
- This tab is special. It performs calculations on-the-fly:
    - `df["total_amount"].sum()`: Shows total volume.
    - `df["customer_id"].nunique()`: Shows how many customers were active.
- **Charts**:
    - `st.area_chart`: Shows daily volume trends.
    - `st.bar_chart`: Shows which customers are the "Whales" (top spenders).

---

## **4. The Refresh Mechanism**
```python
if st.sidebar.button("🚀 Refresh Pipeline"):
    st.cache_resource.clear()
    st.rerun()
```
- Clicking this clears the connection cache and forces the dashboard to look for new folders in MinIO. This is how you see your latest Airflow run.
