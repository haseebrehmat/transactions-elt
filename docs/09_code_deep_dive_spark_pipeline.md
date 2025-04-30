# 09 - Code Deep Dive: The Transformation Jobs

The pipeline consists of several scripts that take data from the "Raw" stage and refine it step-by-step. Each script follows a similar pattern but performs a unique business logic.

---

## **1. Basic Cleansing (`clean.py`)**

### **Method: `clean_transactions(execution_folder)`**
- **Logic**: 
    - Loads data from `iceberg.bank.raw_transactions`.
    - **`df.dropna(subset=[...])`**: Drops any transaction that is missing a ID, Customer ID, Amount, or Date. This prevents "garbage" data from breaking calculations later.
    - **`upper(trim(col(...)))`**: Removes accidental spaces at the beginning/end of strings and makes them uppercase for consistency.
- **Output**: Writes to `iceberg.bank.clean_transactions` in `overwrite` mode.

---

## **2. Normalization (`normalize.py`)**

### **Method: `normalize_transactions(execution_folder)`**
- **Logic**:
    - **Casting**: Converts `txn_amount` to a Decimal with 2 decimal places (`18,2`).
    - **Date Conversion**: Converts the `txn_date` string into a real Spark `Timestamp` using `to_timestamp`.
    - **Cleanup**: Uses `.drop("txn_date", "txn_type")` to remove the old unformatted columns, leaving only the "normalized" ones.
- **Output**: Writes to `iceberg.bank.normalized_transactions`.

---

## **3. Success Filtering (`filter.py`)**

### **Method: `filter_success(execution_folder)`**
- **Logic**:
    - This is a simple but critical business rule.
    - **`df.filter(col("status") != "FAILED")`**: Excludes any transaction that didn't go through.
- **Output**: Writes to `iceberg.bank.success_transactions`.

---

## **4. Feature Enrichment (`enrich.py`)**

### **Method: `enrich_transactions(execution_folder)`**
- **Logic**:
    - **`to_date(col("txn_ts"))`**: Creates a `txn_day` column (Year-Month-Day) which is easier to group by than a timestamp.
    - **High Value Logic**: Uses `when(col("txn_amount") > 10000, True).otherwise(False)` to "tag" large transactions.
- **Output**: Writes to `iceberg.bank.enriched_transactions`.

---

## **5. Aggregation (`aggregate.py`)**

### **Method: `aggregate_daily(execution_folder)`**
- **Logic**:
    - This is the final step that produces "Ready for Dashboard" data.
    - **`groupBy("txn_day", "customer_id")`**: Groups all records by day and client.
    - **`.agg(...)`**: 
        - `count("txn_id")`: How many times did they spend?
        - `sum("txn_amount")`: How much total money moved?
        - `count_if(col("is_high_value"))`: How many times was it over $10k?
- **Output**: Writes to `iceberg.bank.daily_transaction_summary`.

---

## **Common Pattern in all jobs:**
1.  **Initialize**: `spark = get_spark_session(...)`.
2.  **Input**: Read from the *previous* stage's Iceberg table.
3.  **Process**: Apply the specific logic described above.
4.  **Snapshot**: `write_stage_snapshot(...)` for debugging.
5.  **Output**: Use `write_iceberg_table(...)` to save the result.
6.  **Close**: `spark.stop()`.
