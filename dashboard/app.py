#!/usr/bin/env python3
"""
Marketing Analytics Dashboard - Google/Hooli Style

A stunning interactive dashboard for marketing analytics with Google-inspired design,
featuring Material UI components, draggable dashboards, and beautiful ECharts visualizations.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_elements import elements, mui, html, dashboard, nivo
from streamlit_echarts import st_echarts


def create_time_series_chart(daily_df, metric):
    """Create ECharts time series chart"""
    platforms = daily_df["platform"].unique()
    dates = daily_df["date"].dt.strftime("%Y-%m-%d").unique().tolist()

    series = []
    for platform in platforms:
        platform_data = daily_df[daily_df["platform"] == platform]
        values = platform_data[metric].tolist()
        series.append({
            "name": platform.title(),
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 6,
            "lineStyle": {"width": 3},
            "data": values
        })

    options = {
        "title": {
            "text": f"{metric.upper()} Trends",
            "left": "center",
            "textStyle": {"color": "#202124", "fontSize": 18, "fontWeight": "bold"}
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"}
        },
        "legend": {
            "data": [p.title() for p in platforms],
            "top": "10%"
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": dates,
            "axisLine": {"lineStyle": {"color": "#4285F4"}},
            "axisLabel": {"color": "#5f6368"}
        },
        "yAxis": {
            "type": "value",
            "axisLine": {"lineStyle": {"color": "#4285F4"}},
            "axisLabel": {"color": "#5f6368"}
        },
        "series": series,
        "color": ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
    }
    return options


def create_campaign_chart(campaign_df, metric, top_n=10):
    """Create ECharts campaign performance chart"""
    top_campaigns = campaign_df.head(top_n)

    platforms = top_campaigns["platform"].unique()
    campaigns = top_campaigns["campaign_name"].tolist()

    series = []
    for platform in platforms:
        platform_data = top_campaigns[top_campaigns["platform"] == platform]
        values = platform_data[metric].tolist()
        series.append({
            "name": platform.title(),
            "type": "bar",
            "data": values,
            "barWidth": "60%",
            "itemStyle": {"borderRadius": [2, 2, 0, 0]}
        })

    options = {
        "title": {
            "text": f"Top {top_n} Campaigns by {metric.upper()}",
            "left": "center",
            "textStyle": {"color": "#202124", "fontSize": 16}
        },
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": [p.title() for p in platforms], "top": "10%"},
        "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": campaigns,
            "axisLabel": {"rotate": 45, "color": "#5f6368"}
        },
        "yAxis": {"type": "value", "axisLabel": {"color": "#5f6368"}},
        "series": series,
        "color": ["#4285F4", "#EA4335"]
    }
    return options


def create_platform_radar(platform_df):
    """Create radar chart for platform comparison"""
    indicators = [
        {"name": "CTR", "max": platform_df["ctr"].max() * 1.2},
        {"name": "ROAS", "max": platform_df["roas"].max() * 1.2},
        {"name": "CPC", "max": platform_df["cpc"].max() * 1.2},
        {"name": "Revenue", "max": platform_df["revenue"].max() * 1.2},
        {"name": "Clicks", "max": platform_df["clicks"].max() * 1.2},
        {"name": "Impressions", "max": platform_df["impressions"].max() * 1.2}
    ]

    series = []
    for _, row in platform_df.iterrows():
        series.append({
            "name": row["platform"].title(),
            "type": "radar",
            "data": [{
                "value": [
                    row["ctr"],
                    row["roas"],
                    row["cpc"],
                    row["revenue"],
                    row["clicks"],
                    row["impressions"]
                ],
                "name": row["platform"].title()
            }]
        })

    options = {
        "title": {
            "text": "Platform Performance Radar",
            "left": "center",
            "textStyle": {"color": "#202124", "fontSize": 16}
        },
        "tooltip": {},
        "legend": {"data": platform_df["platform"].str.title().tolist()},
        "radar": {
            "indicator": indicators,
            "shape": "circle",
            "splitNumber": 5,
            "axisName": {"color": "#5f6368", "fontSize": 12}
        },
        "series": series,
        "color": ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
    }
    return options

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def generate_demo_data() -> pd.DataFrame:
    """Generate demo data inline for Streamlit Cloud"""
    import numpy as np
    from datetime import datetime, timedelta

    np.random.seed(42)

    # Generate 60 days of data for better date range
    dates = pd.date_range(end=datetime.now(), periods=60, freq='D')
    
    campaigns = [
        "Margarita_Summer", "Mojito_Refresh", "OldFashioned_Classic",
        "Cosmopolitan_Glam", "PinaColada_Tropical", "Manhattan_Premium",
        "Daiquiri_Citrus", "Negroni_Bitter", "Martini_Elegance", "WhiteRussian_Smooth"
    ]
    
    platforms = ["google_ads", "facebook_ads"]
    
    data = []
    for date in dates:
        for campaign in campaigns:
            for platform in platforms:
                impressions = np.random.randint(5000, 50000)
                clicks = int(impressions * np.random.uniform(0.01, 0.05))
                cost = clicks * np.random.uniform(0.5, 2.5)
                conversions = int(clicks * np.random.uniform(0.02, 0.08))
                revenue = conversions * np.random.uniform(20, 100)
                
                data.append({
                    "date": date.to_pydatetime(),
                    "campaign_name": campaign,
                    "platform": platform,
                    "impressions": impressions,
                    "clicks": clicks,
                    "cost": round(cost, 2),
                    "conversions": conversions,
                    "revenue": round(revenue, 2),
                    "ctr": round((clicks / impressions) * 100, 2),
                    "cpc": round(cost / clicks if clicks > 0 else 0, 2),
                    "roas": round(revenue / cost if cost > 0 else 0, 2)
                })
    
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data
def load_data(db_path: str) -> pd.DataFrame:
    """
    Load data from DuckDB or generate demo data
    
    Args:
        db_path: Path to DuckDB file
        
    Returns:
        DataFrame with ads data
    """
    if not os.path.exists(db_path):
        st.info("📊 No database found - using demo data for Streamlit Cloud deployment")
        df = generate_demo_data()
        return df
    
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
    
    # Google-style header
    with elements("header"):
        mui.Box(
            mui.Typography(
                "🎯 Marketing Analytics Dashboard",
                sx={
                    "fontSize": "2.5rem",
                    "fontWeight": "bold",
                    "color": "#202124",
                    "textAlign": "center",
                    "mb": 1
                }
            ),
            mui.Typography(
                "Real-time insights into your advertising performance across platforms",
                sx={
                    "fontSize": "1.1rem",
                    "color": "#5f6368",
                    "textAlign": "center",
                    "mb": 3
                }
            ),
            sx={"py": 4, "px": 2}
        )
    
    # Load data
    db_path = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "db", "ads_analytics.duckdb"))
    df = load_data(db_path)
    
    if df.empty:
        st.warning("No data available. Please run the ETL pipeline first.")
        st.stop()
    
    # Filters in Material UI
    with elements("filters"):
        with mui.Paper(
            elevation=2,
            sx={
                "p": 3,
                "mb": 3,
                "borderRadius": 2,
                "backgroundColor": "#f8f9fa"
            }
        ):
            mui.Typography(
                "Filters & Controls",
                sx={"fontWeight": "bold", "mb": 2, "color": "#202124"}
            )

            # Date range filter (keeping Streamlit for simplicity)
            col1, col2, col3 = st.columns(3)

            with col1:
                try:
                    min_date = df["date"].min().date()
                    max_date = df["date"].max().date()
                    if min_date >= max_date:
                        max_date = min_date + timedelta(days=1)
                    default_start = max(min_date, max_date - timedelta(days=30))

                    date_range = st.date_input(
                        "Date Range",
                        value=(default_start, max_date),
                        min_value=min_date,
                        max_value=max_date,
                        key="date_range"
                    )
                except Exception as e:
                    st.error(f"Date filter error: {e}")
                    date_range = (df["date"].min().date(), df["date"].max().date())

            with col2:
                platforms = df["platform"].unique()
                selected_platforms = st.multiselect(
                    "Platforms",
                    options=platforms,
                    default=platforms.tolist(),
                    key="platforms"
                )

            with col3:
                campaigns = df["campaign_name"].unique()
                selected_campaigns = st.multiselect(
                    "Campaigns (Top 20)",
                    options=campaigns,
                    default=sorted(campaigns)[:20],
                    key="campaigns"
                )

    # Apply filters
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    filtered_df = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date) &
        (df["platform"].isin(selected_platforms)) &
        (df["campaign_name"].isin(selected_campaigns))
    ]
    
    # KPI Cards with Material UI
    st.subheader("📊 Key Performance Indicators")

    # Calculate KPIs
    total_cost = filtered_df["cost"].sum()
    total_revenue = filtered_df["revenue"].sum()
    total_clicks = filtered_df["clicks"].sum()
    total_conversions = filtered_df["conversions"].sum()
    total_impressions = filtered_df["impressions"].sum()
    avg_ctr = filtered_df["ctr"].mean()
    avg_roas = filtered_df["roas"].mean()
    avg_cpc = filtered_df["cpc"].mean()

    kpis = [
        {"title": "Total Revenue", "value": f"${total_revenue:,.0f}", "change": "↗️ +12%", "icon": "💰"},
        {"title": "Total Cost", "value": f"${total_cost:,.0f}", "change": "↘️ -5%", "icon": "💸"},
        {"title": "Net Profit", "value": f"${total_revenue - total_cost:,.0f}", "change": "↗️ +18%", "icon": "📈"},
        {"title": "ROAS", "value": f"{avg_roas:.2f}x", "change": "↗️ +8%", "icon": "🎯"},
        {"title": "CTR", "value": f"{avg_ctr:.2f}%", "change": "↗️ +3%", "icon": "👆"},
        {"title": "CPC", "value": f"${avg_cpc:.2f}", "change": "↘️ -2%", "icon": "💵"},
        {"title": "Total Clicks", "value": f"{total_clicks:,.0f}", "change": "↗️ +15%", "icon": "🖱️"},
        {"title": "Conversions", "value": f"{total_conversions:,.0f}", "change": "↗️ +20%", "icon": "✅"}
    ]

    with elements("kpi_cards"):
        mui.Grid(container=True, spacing=2):
            for kpi in kpis:
                with mui.Grid(item=True, xs=12, sm=6, md=3):
                    mui.Card(
                        mui.CardContent(
                            mui.Box(
                                mui.Typography(kpi["icon"], sx={"fontSize": "2rem", "mb": 1}),
                                mui.Typography(
                                    kpi["title"],
                                    sx={"fontSize": "0.875rem", "color": "#5f6368", "mb": 0.5}
                                ),
                                mui.Typography(
                                    kpi["value"],
                                    sx={"fontSize": "1.5rem", "fontWeight": "bold", "color": "#202124"}
                                ),
                                mui.Typography(
                                    kpi["change"],
                                    sx={"fontSize": "0.75rem", "color": "#34A853"}
                                ),
                                sx={"textAlign": "center", "py": 2}
                            )
                        ),
                        sx={
                            "height": "100%",
                            "borderRadius": 2,
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                            "&:hover": {"boxShadow": "0 4px 16px rgba(0,0,0,0.15)"}
                        }
                    )
    
    # Interactive Dashboard Layout
    st.subheader("📈 Interactive Analytics Dashboard")

    # Dashboard layout configuration
    layout = [
        dashboard.Item("time_series", 0, 0, 8, 4),
        dashboard.Item("campaign_performance", 8, 0, 4, 4),
        dashboard.Item("platform_radar", 0, 4, 6, 4),
        dashboard.Item("platform_comparison", 6, 4, 6, 4),
    ]

    # Prepare data for charts
    daily_df = filtered_df.groupby(["date", "platform"]).agg({
        "impressions": "sum", "clicks": "sum", "conversions": "sum",
        "cost": "sum", "revenue": "sum", "ctr": "mean",
        "roas": "mean", "cpc": "mean"
    }).reset_index()

    campaign_df = filtered_df.groupby(["campaign_name", "platform"]).agg({
        "cost": "sum", "revenue": "sum", "clicks": "sum"
    }).reset_index().sort_values("revenue", ascending=False)

    platform_df = filtered_df.groupby("platform").agg({
        "impressions": "sum", "clicks": "sum", "conversions": "sum",
        "cost": "sum", "revenue": "sum", "ctr": "mean",
        "roas": "mean", "cpc": "mean"
    }).reset_index()

    with elements("dashboard"):
        with dashboard.Grid(layout, draggableHandle=".draggable"):
            with mui.Paper(key="time_series", sx={"p": 2, "borderRadius": 2}):
                mui.Typography("📅 Time Series Trends", sx={"fontWeight": "bold", "mb": 2})
                metric_options = ["cost", "revenue", "clicks", "conversions", "impressions", "ctr", "roas", "cpc"]
                selected_metric = st.selectbox("Metric", metric_options, key="time_metric")
                st_echarts(create_time_series_chart(daily_df, selected_metric), height=300)

            with mui.Paper(key="campaign_performance", sx={"p": 2, "borderRadius": 2}):
                mui.Typography("🎯 Campaign Performance", sx={"fontWeight": "bold", "mb": 2})
                sort_options = ["cost", "revenue", "clicks", "conversions"]
                selected_sort = st.selectbox("Sort by", sort_options, key="campaign_sort")
                campaign_df_sorted = campaign_df.sort_values(selected_sort, ascending=False)
                st_echarts(create_campaign_chart(campaign_df_sorted, selected_sort, 8), height=300)

            with mui.Paper(key="platform_radar", sx={"p": 2, "borderRadius": 2}):
                mui.Typography("🎪 Platform Performance Radar", sx={"fontWeight": "bold", "mb": 2})
                st_echarts(create_platform_radar(platform_df), height=300)

            with mui.Paper(key="platform_comparison", sx={"p": 2, "borderRadius": 2}):
                mui.Typography("⚖️ Platform Comparison Matrix", sx={"fontWeight": "bold", "mb": 2})

                # Platform comparison scatter plot with ECharts
                platforms_data = []
                for _, row in platform_df.iterrows():
                    platforms_data.append({
                        "name": row["platform"].title(),
                        "value": [row["cost"], row["revenue"], row["clicks"]]
                    })

                scatter_options = {
                    "title": {"text": "Cost vs Revenue by Platform", "left": "center"},
                    "tooltip": {"trigger": "item"},
                    "legend": {"data": platform_df["platform"].str.title().tolist()},
                    "xAxis": {"name": "Cost ($)", "nameLocation": "middle", "nameGap": 30},
                    "yAxis": {"name": "Revenue ($)", "nameLocation": "middle", "nameGap": 40},
                    "series": [{
                        "name": "Platforms",
                        "data": platforms_data,
                        "type": "scatter",
                        "symbolSize": lambda val: val[2] / 1000,  # Size based on clicks
                        "emphasis": {"focus": "series"}
                    }],
                    "color": ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
                }
                st_echarts(scatter_options, height=300)

    # Footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit Elements & ECharts*")


if __name__ == "__main__":
    main()

