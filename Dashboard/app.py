import streamlit as st
import pandas as pd
import plotly.express as px
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Real Estate Business Dashboard",
    page_icon="🏢",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🏢 Real Estate Business Dashboard")
st.markdown("### Business Analyst Project")

st.info(
    """This interactive dashboard provides insights into **real estate sales, customer segmentation, regional performance, and client behavior** using Streamlit and Plotly. Users can filter the data dynamically and download customized reports for further analysis.
"""
)


# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("final_real_estate_data.csv")
# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["country"].unique().tolist())
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["region"].unique().tolist())
)

selected_client = st.sidebar.selectbox(
    "Client Type",
    ["All"] + sorted(df["client_type"].unique().tolist())
)

# Apply Filters
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if selected_client != "All":
    filtered_df = filtered_df[filtered_df["client_type"] == selected_client]

# -----------------------------
# KPI Cards
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)
# -----------------------------
# Dataset Preview
# -----------------------------

st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏠 Total Properties",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "💰 Average Sale Price",
        f"₹{filtered_df['sale_price'].mean():,.0f}"
    )

with col3:
    st.metric(
        "⭐ Average Satisfaction",
        f"{filtered_df['satisfaction_score'].mean():.2f} / 10"
    )

with col4:
    st.metric(
        "💵 Total Revenue",
        f"₹{filtered_df['sale_price'].sum():,.0f}"
    )

# -----------------------------
# Rename Cluster Labels
# -----------------------------

cluster_labels = {
    0: "🏡 Standard Home Buyers",
    1: "💎 Luxury Buyers",
    2: "💼 Value Buyers",
    3: "💰 Budget Buyers"
}

filtered_df["Cluster_Name"] = filtered_df["Cluster"].map(cluster_labels)

# -----------------------------
# Rename Client Type Labels
# -----------------------------

client_labels = {
    0: "Client Type A",
    1: "Client Type B"
}

filtered_df["Client_Type_Name"] = filtered_df["client_type"].map(client_labels)

# =====================================================
# CHARTS
# =====================================================

col1, col2 = st.columns(2)

# -----------------------------
# Chart 1
# -----------------------------
with col1:

    st.subheader("📊 Property Sale Price Distribution")

    fig = px.histogram(
        filtered_df,
        x="sale_price",
        nbins=20,
        title="Distribution of Property Sale Prices"
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="sale_price_chart"
    )

# -----------------------------
# Chart 2
# -----------------------------
with col2:

    st.subheader("🌍 Top 10 Regions by Total Sales")

    region_sales = (
        filtered_df.groupby("region")["sale_price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        region_sales,
        x="region",
        y="sale_price",
        color="sale_price",
        title="Top 10 Regions by Total Sales",
        text="sale_price",
        color_continuous_scale="Blues"
    )

    fig2.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig2.update_layout(
        height=450,
        xaxis_title="Region",
        yaxis_title="Total Sales (₹)",
        xaxis_tickangle=-30,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="region_sales_chart"
    )
# =====================================================

col3, col4 = st.columns(2)

# -----------------------------
# Chart 3
# -----------------------------
with col3:

    st.subheader("👥 Client Type Distribution")

    client_type = (
        filtered_df["Client_Type_Name"]
        .value_counts()
        .reset_index()
    )

    client_type.columns = ["Client Type", "Count"]

    fig3 = px.bar(
        client_type,
        x="Client Type",
        y="Count",
        color="Client Type",
        text="Count",
        title="Client Type Distribution"
    )

    fig3.update_traces(textposition="outside")

    fig3.update_layout(
        showlegend=False,
        height=450
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        key="client_type_chart"
    )

# -----------------------------
# Chart 4
# -----------------------------
with col4:

    st.subheader("🏘️ Customer Segment Distribution")

    cluster_data = (
        filtered_df["Cluster_Name"]
        .value_counts()
        .reset_index()
    )

    cluster_data.columns = [
        "Customer Segment",
        "Number of Customers"
    ]

    fig4 = px.bar(
        cluster_data,
        x="Number of Customers",
        y="Customer Segment",
        orientation="h",
        color="Customer Segment",
        text="Number of Customers",
        title="Customer Segment Distribution"
    )

    fig4.update_traces(textposition="outside")

    fig4.update_layout(
        showlegend=False,
        height=450
    )

    st.plotly_chart(
        fig4,
        use_container_width=True,
        key="cluster_chart"
    )
# -----------------------------
# Download Filtered Dataset
# -----------------------------

st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_real_estate_data.csv",
    mime="text/csv"
)

# -----------------------------
# Business Insights
# -----------------------------

st.markdown("---")
st.subheader("📌 Business Insights")

highest_region = (
    filtered_df.groupby("region")["sale_price"]
    .sum()
    .idxmax()
)

largest_cluster = (
    filtered_df["Cluster_Name"]
    .value_counts()
    .idxmax()
)

largest_client = (
    filtered_df["Client_Type_Name"]
    .value_counts()
    .idxmax()
)

average_price = filtered_df["sale_price"].mean()

st.info(f"""
## 📌 Business Insights

🏆 **Highest Revenue Region:** {highest_region}

💰 **Average Property Price:** ₹{average_price:,.0f}

🏘 **Largest Customer Segment:** {largest_cluster}

👥 **Most Common Client Type:** {largest_client}

📊 Insights update automatically whenever filters are changed.
""")

st.markdown("---")
st.caption("Developed by Vinayak Awasthi | Business Analyst Internship Project | Streamlit Dashboard")