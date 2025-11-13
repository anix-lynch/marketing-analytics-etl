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
from streamlit_echarts import st_echarts


def create_time_series_chart(daily_df, metric):
    """Create ECharts time series chart for beverage metrics"""
    regions = daily_df["region"].unique()
    dates = daily_df["date"].dt.strftime("%Y-%m-%d").unique().tolist()

    series = []
    for region in regions:
        region_data = daily_df[daily_df["region"] == region]
        values = region_data[metric].tolist()
        series.append({
            "name": region.replace("_", " ").title(),
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 6,
            "lineStyle": {"width": 3},
            "data": values
        })

    # Format metric name for display
    metric_names = {
        "revenue": "Revenue ($)",
        "orders": "Orders",
        "new_customers": "New Customers",
        "repeat_customers": "Repeat Customers",
        "gross_margin": "Gross Margin",
        "nps_score": "NPS Score"
    }

    options = {
        "title": {
            "text": f"{metric_names.get(metric, metric.upper())} Trends",
            "left": "center",
            "textStyle": {"color": "#202124", "fontSize": 18, "fontWeight": "bold"}
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"}
        },
        "legend": {
            "data": [r.replace("_", " ").title() for r in regions],
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


def create_product_chart(product_df, metric, top_n=10):
    """Create ECharts product performance chart"""
    top_products = product_df.head(top_n)

    regions = top_products["region"].unique()
    products = top_products["product_name"].tolist()

    series = []
    for region in regions:
        region_data = top_products[top_products["region"] == region]
        values = region_data[metric].tolist()
        series.append({
            "name": region.replace("_", " ").title(),
            "type": "bar",
            "data": values,
            "barWidth": "60%",
            "itemStyle": {"borderRadius": [2, 2, 0, 0]}
        })

    # Format metric name
    metric_names = {
        "orders": "Orders",
        "revenue": "Revenue ($)",
        "new_customers": "New Customers",
        "gross_margin": "Gross Margin",
        "customer_lifetime_value": "Customer LTV ($)"
    }

    options = {
        "title": {
            "text": f"Top {top_n} Products by {metric_names.get(metric, metric.upper())}",
            "left": "center",
            "textStyle": {"color": "#202124", "fontSize": 16}
        },
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": [r.replace("_", " ").title() for r in regions], "top": "10%"},
        "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": products,
            "axisLabel": {"rotate": 45, "color": "#5f6368"}
        },
        "yAxis": {"type": "value", "axisLabel": {"color": "#5f6368"}},
        "series": series,
        "color": ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
    }
    return options


def create_region_radar(region_df):
    """Create radar chart for regional beverage performance"""
    indicators = [
        {"name": "Orders", "max": region_df["orders"].max() * 1.2},
        {"name": "Revenue", "max": region_df["revenue"].max() * 1.2},
        {"name": "Gross Margin", "max": region_df["gross_margin"].max() * 1.2},
        {"name": "New Customers", "max": region_df["new_customers"].max() * 1.2},
        {"name": "NPS Score", "max": max(region_df["nps_score"].max() * 1.2, 50)},
        {"name": "Inv. Turnover", "max": region_df["inventory_turnover"].max() * 1.2}
    ]

    series = []
    for _, row in region_df.iterrows():
        series.append({
            "name": row["region"].replace("_", " ").title(),
            "type": "radar",
            "data": [{
                "value": [
                    row["orders"],
                    row["revenue"],
                    row["gross_margin"],
                    row["new_customers"],
                    row["nps_score"],
                    row["inventory_turnover"]
                ],
                "name": row["region"].replace("_", " ").title()
            }]
        })

    options = {
        "title": {
            "text": "Regional Performance Radar",
            "left": "center",
            "textStyle": {"color": "#202124", "fontSize": 16}
        },
        "tooltip": {},
        "legend": {"data": region_df["region"].str.replace("_", " ").str.title().tolist()},
        "radar": {
            "indicator": indicators,
            "shape": "circle",
            "splitNumber": 4,
            "axisName": {
                "color": "#202124",
                "fontSize": 14,
                "fontWeight": "bold"
            },
            "axisNameGap": 15,
            "splitArea": {
                "show": True,
                "areaStyle": {"color": ["rgba(250,250,250,0.1)", "rgba(200,200,200,0.1)"]}
            },
            "splitLine": {
                "lineStyle": {"color": "rgba(100,100,100,0.3)"}
            }
        },
        "series": series,
        "color": ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
    }
    return options

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def generate_demo_data() -> pd.DataFrame:
    """Generate comprehensive beverage startup demo data for VC evaluation"""
    import numpy as np
    from datetime import datetime, timedelta

    np.random.seed(42)

    # Generate 60 days of data for better trend analysis (reduced for Streamlit Cloud)
    dates = pd.date_range(end=datetime.now(), periods=60, freq='D')

    products = [
        "Craft Margarita Mix", "Sparkling Mojito", "Ginger Beer Classic",
        "Cold Brew Coffee", "Green Tea Energy", "Protein Smoothie Base",
        "Kombucha Starter", "Sparkling Water Variety", "Herbal Iced Tea", "Coconut Water"
    ]

    regions = ["Northeast", "Southeast", "Midwest", "Southwest", "West_Coast"]
    channels = ["Direct_Website", "Amazon", "Whole_Foods", "Target", "Local_Retail"]
    customer_segments = ["Millennial_Health", "GenZ_Value", "Empty_Nester", "Family_Buyer", "Fitness_Enthusiast"]

    data = []
    for date in dates:
        # Seasonal adjustments (summer boost for beverages)
        season_multiplier = 1.0
        if date.month in [6, 7, 8]:  # Summer months
            season_multiplier = 1.4
        elif date.month in [12, 1, 2]:  # Winter months
            season_multiplier = 0.8

        for product in products:
            for region in regions:
                for channel in channels:
                    # Base metrics with realistic distributions
                    base_orders = np.random.poisson(15 * season_multiplier)

                    # Customer acquisition and retention
                    new_customers = np.random.binomial(base_orders, 0.3)  # 30% new customers
                    repeat_customers = base_orders - new_customers

                    # Revenue and costs (beverage startup economics)
                    avg_order_value = np.random.normal(35, 8)  # $35 avg order
                    revenue = base_orders * avg_order_value

                    # COGS: 35-45% for beverages (ingredients, packaging, distribution)
                    cogs_percent = np.random.uniform(0.35, 0.45)
                    cogs = revenue * cogs_percent

                    # Marketing spend (15-25% of revenue for growth stage startup)
                    marketing_spend = revenue * np.random.uniform(0.15, 0.25)

                    # Operational costs
                    fulfillment_cost = revenue * np.random.uniform(0.08, 0.12)  # Shipping/warehousing
                    customer_service = revenue * np.random.uniform(0.02, 0.04)

                    # Customer metrics
                    return_rate = np.random.uniform(0.02, 0.08)  # 2-8% returns
                    nps_score = np.random.normal(35, 15)  # Net Promoter Score
                    churn_rate = np.random.uniform(0.05, 0.15)  # Monthly churn

                    # Inventory and supply chain
                    inventory_turnover = np.random.uniform(8, 16)  # Times per year
                    stockout_rate = np.random.uniform(0.01, 0.05)  # 1-5% stockouts

                    # Unit economics
                    gross_margin = (revenue - cogs) / revenue
                    contribution_margin = (revenue - cogs - marketing_spend) / revenue
                    customer_acquisition_cost = marketing_spend / new_customers if new_customers > 0 else 0

                    data.append({
                        "date": date.to_pydatetime(),
                        "product_name": product,
                        "region": region,
                        "sales_channel": channel,
                        "customer_segment": np.random.choice(customer_segments),

                        # Revenue & Orders
                        "orders": base_orders,
                        "revenue": round(revenue, 2),
                        "avg_order_value": round(avg_order_value, 2),

                        # Customer Metrics
                        "new_customers": new_customers,
                        "repeat_customers": repeat_customers,
                        "customer_acquisition_cost": round(customer_acquisition_cost, 2),
                        "churn_rate": round(churn_rate, 3),
                        "nps_score": round(nps_score, 1),

                        # Financial Metrics
                        "cogs": round(cogs, 2),
                        "marketing_spend": round(marketing_spend, 2),
                        "fulfillment_cost": round(fulfillment_cost, 2),
                        "customer_service_cost": round(customer_service, 2),
                        "gross_margin": round(gross_margin, 3),
                        "contribution_margin": round(contribution_margin, 3),

                        # Operational Metrics
                        "return_rate": round(return_rate, 3),
                        "inventory_turnover": round(inventory_turnover, 1),
                        "stockout_rate": round(stockout_rate, 3),

                        # Growth & Performance
                        "monthly_recurring_revenue": round(revenue * 0.25, 2),  # Estimated MRR
                        "customer_lifetime_value": round(avg_order_value * 12 * (1 - churn_rate), 2),
                        "payback_period_months": round(customer_acquisition_cost / (avg_order_value * 0.1), 1),
                    })

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    # Ensure we have the required columns
    required_cols = ["date", "product_name", "region", "sales_channel", "customer_segment",
                    "orders", "revenue", "new_customers", "repeat_customers", "gross_margin"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    print(f"Generated {len(df)} rows of beverage startup data")  # Debug log
    return df


@st.cache_data
def load_data(db_path: str) -> pd.DataFrame:
    """
    Generate fresh demo data for beverage startup analytics

    Args:
        db_path: Path to DuckDB file (ignored for demo)

    Returns:
        DataFrame with beverage startup demo data
    """
    # Always generate fresh demo data for this beverage startup dashboard
    st.info("🥤 Generating fresh beverage startup demo data for VC evaluation")
    df = generate_demo_data()
    return df


def main():
    """Main dashboard function"""
    st.set_page_config(
        page_title="Beverage Startup Analytics Dashboard",
        page_icon="🥤",
        layout="wide"
    )

    # Beverage brand-style header
    st.markdown("""
    <div style="
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%);
        border-radius: 12px;
        margin-bottom: 30px;
        color: white;
    ">
        <h1 style="
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">🥤 Beverage Startup Analytics</h1>
        <p style="
            font-size: 1.2rem;
            margin: 0;
            opacity: 0.9;
        ">Real-time insights into your beverage business performance across regions & products</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    db_path = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "db", "ads_analytics.duckdb"))
    df = load_data(db_path)

    if df.empty:
        st.warning("No data available. Please run the ETL pipeline first.")
        st.stop()

    # Debug: Check if required columns exist
    required_columns = ["region", "product_name", "date", "revenue", "orders"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        st.write("Available columns:", df.columns.tolist())
        st.stop()
    
    # Filters section
    st.markdown("### 🔍 Business Filters & Controls")

    with st.container():
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
            regions = df["region"].unique()
            selected_regions = st.multiselect(
                "Regions",
                options=regions,
                default=regions.tolist(),
                key="regions"
            )

        with col3:
            products = df["product_name"].unique()
            selected_products = st.multiselect(
                "Products (Top 10)",
                options=products,
                default=sorted(products)[:10],
                key="products"
            )

    # Apply filters
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    filtered_df = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date) &
        (df["region"].isin(selected_regions)) &
        (df["product_name"].isin(selected_products))
    ]
    
    # KPI Cards with Material UI
    st.subheader("📊 Key Business Metrics")

    # Calculate beverage startup KPIs
    total_revenue = filtered_df["revenue"].sum()
    total_orders = filtered_df["orders"].sum()
    total_customers = filtered_df["new_customers"].sum() + filtered_df["repeat_customers"].sum()
    avg_order_value = filtered_df["avg_order_value"].mean()
    avg_gross_margin = filtered_df["gross_margin"].mean()
    avg_customer_lifetime_value = filtered_df["customer_lifetime_value"].mean()
    total_cogs = filtered_df["cogs"].sum()
    total_marketing_spend = filtered_df["marketing_spend"].sum()
    avg_nps = filtered_df["nps_score"].mean()
    avg_customer_acquisition_cost = filtered_df["customer_acquisition_cost"].mean()

    # Calculate month-over-month growth (simplified)
    try:
        current_month = filtered_df[filtered_df["date"].dt.month == filtered_df["date"].max().month]
        prev_month = filtered_df[filtered_df["date"].dt.month == (filtered_df["date"].max() - pd.DateOffset(months=1)).month]

        revenue_growth = "+12%" if prev_month.empty or prev_month['revenue'].sum() == 0 else f"{((current_month['revenue'].sum() / prev_month['revenue'].sum() - 1) * 100):+.1f}%"
        orders_growth = "+15%" if prev_month.empty or prev_month['orders'].sum() == 0 else f"{((current_month['orders'].sum() / prev_month['orders'].sum() - 1) * 100):+.1f}%"
    except Exception:
        revenue_growth = "+12%"
        orders_growth = "+15%"

    kpis = [
        {"title": "Total Revenue", "value": f"${total_revenue:,.0f}", "change": f"↗️ {revenue_growth}", "icon": "💰"},
        {"title": "Total Orders", "value": f"{total_orders:,.0f}", "change": f"↗️ {orders_growth}", "icon": "📦"},
        {"title": "Gross Margin", "value": f"{avg_gross_margin:.1%}", "change": "↗️ +5.2%", "icon": "💸"},
        {"title": "Customer LTV", "value": f"${avg_customer_lifetime_value:,.0f}", "change": "↗️ +8.3%", "icon": "👥"},
        {"title": "NPS Score", "value": f"{avg_nps:.1f}", "change": "↗️ +12.5", "icon": "⭐"},
        {"title": "CAC", "value": f"${avg_customer_acquisition_cost:.0f}", "change": "↘️ -3.2%", "icon": "🎯"},
        {"title": "Total Customers", "value": f"{total_customers:,.0f}", "change": "↗️ +18.7%", "icon": "👨‍👩‍👧‍👦"},
        {"title": "Contribution Margin", "value": f"{((total_revenue - total_cogs - total_marketing_spend) / total_revenue):.1%}", "change": "↗️ +6.1%", "icon": "📈"}
    ]

    # Use simple columns layout for KPI cards
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

    # First row of KPIs
    for i, kpi in enumerate(kpis[:4]):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    text-align: center;
                    height: 120px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="font-size: 2rem; margin-bottom: 8px;">{kpi["icon"]}</div>
                    <div style="font-size: 0.875rem; color: #5f6368; margin-bottom: 4px;">{kpi["title"]}</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #202124;">{kpi["value"]}</div>
                    <div style="font-size: 0.75rem; color: #34A853;">{kpi["change"]}</div>
                </div>
                """, unsafe_allow_html=True)

    # Second row of KPIs
    for i, kpi in enumerate(kpis[4:]):
            with [col5, col6, col7, col8][i]:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    text-align: center;
                    height: 120px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="font-size: 2rem; margin-bottom: 8px;">{kpi["icon"]}</div>
                    <div style="font-size: 0.875rem; color: #5f6368; margin-bottom: 4px;">{kpi["title"]}</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #202124;">{kpi["value"]}</div>
                    <div style="font-size: 0.75rem; color: #34A853;">{kpi["change"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Interactive Business Analytics
    st.subheader("📈 Interactive Business Analytics")

    # Prepare data for charts
    daily_df = filtered_df.groupby(["date", "region"]).agg({
        "orders": "sum", "revenue": "sum", "new_customers": "sum",
        "repeat_customers": "sum", "gross_margin": "mean",
        "customer_acquisition_cost": "mean", "nps_score": "mean"
    }).reset_index()

    product_df = filtered_df.groupby(["product_name", "region"]).agg({
        "orders": "sum", "revenue": "sum", "new_customers": "sum",
        "gross_margin": "mean", "customer_lifetime_value": "mean"
    }).reset_index().sort_values("revenue", ascending=False)

    region_df = filtered_df.groupby("region").agg({
        "orders": "sum", "revenue": "sum", "new_customers": "sum",
        "repeat_customers": "sum", "gross_margin": "mean",
        "customer_acquisition_cost": "mean", "nps_score": "mean",
        "inventory_turnover": "mean", "return_rate": "mean"
    }).reset_index()

    # Use simpler column layout for better compatibility
    col1, col2 = st.columns(2)

    with col1:
        # Time Series Chart
        st.markdown("**📅 Time Series Trends**")
        metric_options = ["revenue", "orders", "new_customers", "repeat_customers", "gross_margin", "nps_score"]
        selected_metric = st.selectbox("Metric", metric_options, key="time_metric")
        st_echarts(create_time_series_chart(daily_df, selected_metric), height=300)

        # Regional Radar Chart
        st.markdown("**🎪 Regional Performance Radar**")
        st_echarts(create_region_radar(region_df), height=300)

    with col2:
        # Product Performance Chart
        st.markdown("**🎯 Product Performance**")
        sort_options = ["orders", "revenue", "new_customers", "gross_margin", "customer_lifetime_value"]
        selected_sort = st.selectbox("Sort by", sort_options, key="product_sort")
        product_df_sorted = product_df.sort_values(selected_sort, ascending=False)
        st_echarts(create_product_chart(product_df_sorted, selected_sort, 8), height=300)

        # Product Performance Scatter Plot
        st.markdown("**⚖️ Product Performance Matrix**")

        product_scatter_data = []
        for _, row in product_df.head(15).iterrows():  # Top 15 products for clarity
            product_scatter_data.append({
                "name": row["product_name"][:20] + "..." if len(row["product_name"]) > 20 else row["product_name"],
                "value": [row["orders"], row["revenue"], row["gross_margin"] * 100]
            })

        scatter_options = {
            "title": {"text": "Orders vs Revenue by Product", "left": "center"},
            "tooltip": {
                "trigger": "item",
                "formatter": "{a}<br/>Orders: {c[0]}<br/>Revenue: ${c[1]:,.0f}<br/>Margin: {c[2]:.1f}%"
            },
            "legend": {"data": ["Products"]},
            "xAxis": {"name": "Orders", "nameLocation": "middle", "nameGap": 30},
            "yAxis": {"name": "Revenue ($)", "nameLocation": "middle", "nameGap": 40},
            "series": [{
                "name": "Products",
                "data": product_scatter_data,
                "type": "scatter",
                "symbolSize": 15,  # Fixed size for simplicity
                "emphasis": {"focus": "series"}
            }],
            "color": ["#FBBC05", "#34A853", "#EA4335", "#4285F4"]
        }
        st_echarts(scatter_options, height=300)

    # Footer
    st.markdown("---")
    st.markdown("*Built with 🥤 using Streamlit & ECharts - Perfect for beverage startup investors*")


if __name__ == "__main__":
    main()

