# 06 - Advanced Concept: Apache Iceberg

You might be wondering: "Why not just use regular CSV or Parquet files?"

**Apache Iceberg** is a "Table Format." It sits between our data files and Spark to add powerful features that files alone don't have.

## 1. ACID Transactions
In a normal data lake, if a Spark job crashes halfway through writing a file, you end up with "garbage" half-written data.
With Iceberg, the "write" is all-or-nothing. Either it succeeds completely, or it doesn't happen at all.

## 2. Schema Evolution
Imagine you want to start tracking a new column, like `location`.
- With CSVs, adding a column to an old file is a nightmare.
- With Iceberg, you just add it! It handles the complexity of making sure old data and new data work together seamlessly.

## 3. Time Travel
Iceberg keeps track of "Snapshots." 
You can actually ask Spark: "Show me what this table looked like last Tuesday at 4 PM." It can roll back the clock and show you exactly what the data was then.

## 4. Hidden Partitioning
Iceberg is smart. If you search for data from "December 2025," it knows exactly which files to look in and skips the rest. This makes it **super fast** even if you have trillions of transactions.

---
## Summary
By combining **Spark** (Speed), **Airflow** (Control), **Iceberg** (Reliability), and **Streamlit** (Beauty), you've built a professional-grade Data Engineering platform!
