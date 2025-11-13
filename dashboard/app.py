#!/usr/bin/env python3
"""
Marketing Analytics Dashboard

Streamlit dashboard for visualizing Google Ads and Facebook Ads performance.
Shows KPIs, time series trends, campaign breakdowns, and platform comparisons.
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import duckdb

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@st.cache_data
def load_data(db_path: str) -> pd.DataFrame:
    """
    Load data from DuckDB
    
    Args:
        db_path: Path to DuckDB file
        
    Returns:
        DataFrame with ads data
    """
    if not os.path.exists(db_path):
        st.error(f"Database not found at {db_path}. Please run the ETL pipeline first.")
        st.stop()
    
    conn = duckdb.connect(db_path)
    df = conn.execute("SELECT * FROM ads_analytics").df()
    conn.close()
    
    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"])
    
    return df


def main():
    """Main dashboard function"""
    st.set_page_config(
        page_title="Marketing Analytics Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Marketing Analytics Dashboard")
    st.markdown("Google Ads & Facebook Ads Performance Analysis")
    
    # Load data
    db_path = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "db", "ads_analytics.duckdb"))
    df = load_data(db_path)
    
    if df.empty:
        st.warning("No data available. Please run the ETL pipeline first.")
        st.stop()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(max_date - timedelta(days=30), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range
    
    # Platform filter
    platforms = st.sidebar.multiselect(
        "Platform",
        options=df["platform"].unique().tolist(),
        default=df["platform"].unique().tolist()
    )
    
    # Campaign filter
    campaigns = st.sidebar.multiselect(
        "Campaign",
        options=sorted(df["campaign_name"].unique().tolist()),
        default=[]
    )
    
    # Apply filters
    filtered_df = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date) &
        (df["platform"].isin(platforms))
    ]
    
    if campaigns:
        filtered_df = filtered_df[filtered_df["campaign_name"].isin(campaigns)]
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        st.stop()
    
    # KPI Metrics
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cost = filtered_df["cost"].sum()
        st.metric("Total Cost", f"${total_cost:,.2f}")
    
    with col2:
        avg_ctr = filtered_df["ctr"].mean()
        st.metric("Avg CTR", f"{avg_ctr:.2f}%")
    
    with col3:
        avg_roas = filtered_df["roas"].mean()
        st.metric("Avg ROAS", f"{avg_roas:.2f}x")
    
    with col4:
        avg_cpc = filtered_df["cpc"].mean()
        st.metric("Avg CPC", f"${avg_cpc:.2f}")
    
    # Additional KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        total_revenue = filtered_df["revenue"].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col6:
        total_clicks = filtered_df["clicks"].sum()
        st.metric("Total Clicks", f"{total_clicks:,}")
    
    with col7:
        total_conversions = filtered_df["conversions"].sum()
        st.metric("Total Conversions", f"{total_conversions:,}")
    
    with col8:
        total_impressions = filtered_df["impressions"].sum()
        st.metric("Total Impressions", f"{total_impressions:,}")
    
    st.divider()
    
    # Time Series Trends
    st.header("📅 Time Series Trends")
    
    # Aggregate by date
    daily_df = filtered_df.groupby(["date", "platform"]).agg({
        "impressions": "sum",
        "clicks": "sum",
        "conversions": "sum",
        "cost": "sum",
        "revenue": "sum",
        "ctr": "mean",
        "roas": "mean",
        "cpc": "mean"
    }).reset_index()
    
    # Metric selector for time series
    time_metric = st.selectbox(
        "Select Metric",
        options=["cost", "revenue", "clicks", "conversions", "impressions", "ctr", "roas", "cpc"],
        index=0,
        key="time_metric"
    )
    
    # Time series chart
    fig_time = px.line(
        daily_df,
        x="date",
        y=time_metric,
        color="platform",
        title=f"{time_metric.upper()} Trend Over Time",
        labels={time_metric: time_metric.upper(), "date": "Date", "platform": "Platform"}
    )
    fig_time.update_layout(height=400)
    st.plotly_chart(fig_time, use_container_width=True)
    
    st.divider()
    
    # Campaign Breakdown
    st.header("🎯 Campaign Performance")
    
    # Aggregate by campaign
    campaign_df = filtered_df.groupby(["campaign_name", "platform"]).agg({
        "impressions": "sum",
        "clicks": "sum",
        "conversions": "sum",
        "cost": "sum",
        "revenue": "sum",
        "ctr": "mean",
        "roas": "mean",
        "cpc": "mean"
    }).reset_index()
    
    # Sort by cost (or another metric)
    sort_by = st.selectbox(
        "Sort By",
        options=["cost", "revenue", "clicks", "conversions", "roas", "ctr"],
        index=0,
        key="sort_by"
    )
    campaign_df = campaign_df.sort_values(sort_by, ascending=False)
    
    # Campaign breakdown chart
    fig_campaign = px.bar(
        campaign_df.head(20),  # Top 20 campaigns
        x="campaign_name",
        y=sort_by,
        color="platform",
        title=f"Top 20 Campaigns by {sort_by.upper()}",
        labels={sort_by: sort_by.upper(), "campaign_name": "Campaign", "platform": "Platform"}
    )
    fig_campaign.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig_campaign, use_container_width=True)
    
    st.divider()
    
    # Platform Comparison (Stretch Goal)
    st.header("⚖️ Platform Comparison")
    
    # Aggregate by platform
    platform_df = filtered_df.groupby("platform").agg({
        "impressions": "sum",
        "clicks": "sum",
        "conversions": "sum",
        "cost": "sum",
        "revenue": "sum",
        "ctr": "mean",
        "roas": "mean",
        "cpc": "mean"
    }).reset_index()
    
    # Comparison metric selector
    compare_metric = st.selectbox(
        "Compare By",
        options=["cost", "revenue", "clicks", "conversions", "impressions", "ctr", "roas", "cpc"],
        index=0,
        key="compare_metric"
    )
    
    # Platform comparison chart
    fig_compare = px.bar(
        platform_df,
        x="platform",
        y=compare_metric,
        color="platform",
        title=f"Platform Comparison: {compare_metric.upper()}",
        labels={compare_metric: compare_metric.upper(), "platform": "Platform"},
        color_discrete_map={
            "google_ads": "#4285F4",
            "facebook_ads": "#1877F2"
        }
    )
    fig_compare.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # Platform comparison table
    st.subheader("Platform Metrics Summary")
    st.dataframe(
        platform_df.style.format({
            "cost": "${:,.2f}",
            "revenue": "${:,.2f}",
            "ctr": "{:.2f}%",
            "roas": "{:.2f}x",
            "cpc": "${:.2f}",
            "impressions": "{:,.0f}",
            "clicks": "{:,.0f}",
            "conversions": "{:,.0f}"
        }),
        use_container_width=True
    )
    
    st.divider()
    
    # Raw Data Table
    with st.expander("📋 View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    main()

