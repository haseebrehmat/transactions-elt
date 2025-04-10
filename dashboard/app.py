import streamlit as st
import boto3
import pandas as pd
import io
import os
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Banking ETL Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Theme and Styling
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Title styling */
    h1 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.05rem;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00ff88 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
    }

    /* Container styling */
    div[data-testid="metric-container"] {
        background-color: #1e2530;
        border: 1px solid #2d3643;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e2530;
        padding: 10px;
        border-radius: 12px 12px 0 0;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #161b22;
        border-radius: 8px;
        color: #8b949e;
        border: 1px solid transparent;
        transition: all 0.2s ease-in-out;
    }

    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        color: white !important;
        border: 1px solid #3fb950;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Table design */
    .stDataFrame {
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# MinIO Connection
@st.cache_resource
def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "admin"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "password123"),
        region_name="us-east-1",
    )


def list_runs():
    s3 = get_s3_client()
    bucket = "pipeline-runs"
    try:
        response = s3.list_objects_v2(Bucket=bucket, Delimiter="/")
        if "CommonPrefixes" not in response:
            return []
        return sorted(
            [p["Prefix"].strip("/") for p in response["CommonPrefixes"]], reverse=True
        )
    except Exception as e:
        st.error(f"Error connecting to MinIO: {e}")
        return []


def load_data(run_folder, stage_name):
    s3 = get_s3_client()
    bucket = "pipeline-runs"
    prefix = f"{run_folder}/{stage_name}/"
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if "Contents" not in response:
            return None
        csv_file = next(
            (obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".csv")),
            None,
        )
        if not csv_file:
            return None
        obj = s3.get_object(Bucket=bucket, Key=csv_file)
        return pd.read_csv(io.BytesIO(obj["Body"].read()))
    except Exception:
        return None


# Sidebar
st.sidebar.markdown("# 🛡️ Bank Sentinel")
st.sidebar.markdown("### Transaction Analysis Engine")
st.sidebar.markdown("---")

runs = list_runs()

if not runs:
    st.title("🏦 Banking Transactions ETL Pipeline")
    st.info("No pipeline runs found yet. Please trigger the DAG in Airflow.")
    st.stop()

selected_run = st.sidebar.selectbox("Select Pipeline Run", runs)
st.sidebar.markdown(f"**Selected Run ID:**\n`{selected_run}`")

# Main Header
st.title("🏛️ Pipeline Operational Intelligence")
st.markdown(
    "Real-time monitoring and analytics for the distributed transaction ledger."
)


# Define all 7 stages
STAGES = {
    "📥 extraction": "0_extraction",
    "📦 raw ingestion": "1_raw_ingestion",
    "🧹 basic cleansing": "2_basic_cleansing",
    "⚙️ normalization": "3_parsing_normalization",
    "🔍 success only": "4_filter_success",
    "💎 feature enrichment": "5_feature_enrichment",
    "📈 daily aggregation": "6_daily_aggregation",
}

tabs = st.tabs([label.upper() for label in STAGES.keys()])

for i, (label, stage_id) in enumerate(STAGES.items()):
    with tabs[i]:
        df = load_data(selected_run, stage_id)
        if df is not None:
            if stage_id == "6_daily_aggregation":
                st.subheader("🏁 Final Aggregation Results")

                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                total_txns = df["total_txns"].sum()
                total_volume = df["total_amount"].sum()
                high_val_count = df["high_value_count"].sum()
                unique_customers = df["customer_id"].nunique()

                m1.metric("Total txns", f"{total_txns:,}")
                m2.metric("Total volume", f"${total_volume:,.0f}")
                m3.metric("High value", f"{high_val_count:,}")
                m4.metric("Active customers", f"{unique_customers:,}")

                st.markdown("---")

                # Visualizations Row
                v1, v2 = st.columns(2)

                with v1:
                    st.markdown("### 💰 Volume by Date")
                    chart_data = df.groupby("txn_day")["total_amount"].sum()
                    st.area_chart(chart_data)

                with v2:
                    st.markdown("### 🔝 Top Customers (by Volume)")
                    top_cust = (
                        df.groupby("customer_id")["total_amount"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(10)
                    )
                    st.bar_chart(top_cust)

                st.markdown("---")
                st.markdown("### 📋 Detailed Records")
                st.dataframe(df, use_container_width=True)

            else:
                st.subheader(f"Stage: {label.title()}")

                # Stage Quick Metrics
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.metric("Total Rows", f"{len(df):,}")

                st.markdown("### 📑 Data Preview")
                st.dataframe(df.head(100), use_container_width=True)

                # Simple distribution chart for non-aggregated data
                if "status" in df.columns:
                    st.markdown("### 📊 Status Distribution")
                    status_counts = df["status"].value_counts()
                    st.bar_chart(status_counts)

        else:
            st.warning(f"Data for stage '{label}' not found or pipeline still running.")

st.sidebar.markdown("---")
if st.sidebar.button("🚀 Refresh Pipeline", use_container_width=True):
    st.cache_resource.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("System Status: ONLINE")
st.sidebar.caption("Last Sync: " + pd.Timestamp.now().strftime("%H:%M:%S"))
