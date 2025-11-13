# 🔍 Metabase & Apache Superset - CLI-Friendly BI Tools

## Why These Are Perfect For You (vs Tableau/Power BI)

### **Metabase: SQL-First BI Tool**
```
Philosophy: "Write SQL, Get Beautiful Charts"
GUI Work: 20% (mostly SQL writing, minimal drag-and-drop)
CLI Work: 80% (SQL queries, API automation, Docker deployment)
```

### **Apache Superset: Developer-First BI**
```
Philosophy: "Enterprise BI, But For Developers"  
GUI Work: 30% (dashboard assembly, some drag-and-drop)
CLI Work: 70% (Python SDK, API automation, custom visualizations)
```

---

## 🏗️ Metabase Setup (Mac-Friendly)

### **Installation (Docker - CLI!)**
```bash
# Pull and run Metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase

# Access at: http://localhost:3000
```

### **Your Workflow (SQL-Heavy!)**
```sql
-- Write SQL queries (your strength!)
SELECT 
    date,
    campaign_name,
    SUM(impressions) as impressions,
    SUM(clicks) as clicks,
    ROUND(AVG(ctr), 2) as avg_ctr,
    SUM(cost) as total_cost,
    SUM(revenue) as total_revenue,
    ROUND(SUM(revenue)/SUM(cost), 2) as roas
FROM marketing_data
WHERE date >= '2025-08-01'
GROUP BY date, campaign_name
ORDER BY total_revenue DESC;

-- Metabase auto-creates: bar charts, line graphs, tables
-- Minimal GUI: just click "Visualize" button
```

### **Automation Potential**
```bash
# Metabase API for automation
curl -X POST "http://localhost:3000/api/card" \
  -H "X-Metabase-Session: $SESSION_TOKEN" \
  -d '{"name": "Revenue Trend", "dataset_query": {...}}'

# Scheduled reports via cron
0 9 * * * /path/to/generate_metabase_report.sh
```

---

## 🚀 Apache Superset Setup

### **Installation (Python - Your Favorite!)**
```bash
# Install via pip
pip install apache-superset

# Initialize
superset db upgrade
superset init

# Create admin user
superset fab create-admin

# Start server
superset run -p 8088
```

### **Your Workflow (Python + SQL)**
```python
# Python SDK for dashboard creation
from supersetapiclient import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="your-password"
)

# Create dataset programmatically
dataset = client.datasets.create({
    "database": 1,
    "schema": "public", 
    "table_name": "marketing_data"
})

# Create charts via API
chart = client.charts.create({
    "slice_name": "Revenue Trend",
    "datasource_id": dataset.id,
    "datasource_type": "table",
    "viz_type": "line",
    "params": {...}
})

# Build dashboards programmatically
dashboard = client.dashboards.create({
    "dashboard_title": "Marketing Analytics",
    "position_json": {...},
    "css": "..."
})
```

---

## 📊 Comparison: Your Options

| Tool | GUI Work | CLI/SQL Work | Setup Complexity | Automation | Enterprise Ready |
|------|----------|--------------|------------------|------------|-------------------|
| **Tableau** | 90% | 10% | Low | Limited | Yes |
| **Power BI** | 85% | 15% | Low | Limited | Yes |
| **Metabase** | 25% | 75% | Medium | Good | Basic |
| **Superset** | 35% | 65% | High | Excellent | Yes |
| **Streamlit** | 10% | 90% | Low | Excellent | Dev-focused |

---

## 🎯 My Recommendation: Start with Metabase

### **Why Metabase First:**
1. **SQL-Focused**: 80% of work is writing SQL (your strength)
2. **Simple Setup**: Docker one-liner
3. **Quick Results**: Working dashboard in 30 minutes
4. **API Available**: Can automate later
5. **Perfect Bridge**: From your current SQL skills to BI

### **Upgrade to Superset Later:**
- When you want more customization
- Enterprise features needed
- Python SDK for advanced automation

---

## 🔧 Metabase Quick Start for Your Data

### **Step 1: Import Your Data**
```bash
# Your CSV is ready
ls marketing_data_for_bi.csv  # ✅ Already exists
```

### **Step 2: Connect Database**
```sql
-- Metabase will ask for connection
-- Point to your CSV or create SQLite DB
```

### **Step 3: Write SQL Queries**
```sql
-- Revenue by Campaign (your first chart)
SELECT 
    campaign_name,
    SUM(revenue) as total_revenue,
    SUM(cost) as total_cost,
    ROUND(SUM(revenue)/SUM(cost), 2) as roas
FROM marketing_data_for_bi
GROUP BY campaign_name
ORDER BY total_revenue DESC
LIMIT 10;
```

### **Step 4: Metabase Creates Visualization**
- Click "Visualize" → Bar Chart
- Add to Dashboard
- **Done!** (Mostly SQL, minimal GUI)

---

## 💡 Portfolio Addition Strategy

### **Add to Your Resume:**
```
Business Intelligence Tools:
- Metabase: SQL-based dashboard development and automation
- Apache Superset: Python SDK for programmatic BI solutions
- Streamlit: Custom interactive data applications
```

### **Showcase Projects:**
1. **Marketing Analytics (Metabase)**: SQL-driven executive dashboards
2. **Real-time Monitoring (Superset)**: API-automated report generation  
3. **Custom Apps (Streamlit)**: Full-stack data applications

### **Skills Demonstrated:**
- ✅ SQL mastery for business intelligence
- ✅ API-driven BI automation
- ✅ Docker deployment and containerization
- ✅ Enterprise BI tool configuration

---

## 🚀 Why These Beat Tableau/Power BI for You

### **Metabase Advantages:**
- **SQL-Centric**: Write queries, get charts (your workflow!)
- **Open Source**: No license costs
- **API Automation**: Can script dashboard creation
- **Docker Deployment**: Infrastructure as code

### **Superset Advantages:**  
- **Python Native**: Use your favorite language
- **Highly Customizable**: Build exactly what you need
- **Enterprise Features**: Row-level security, etc.
- **Active Community**: Apache project support

### **Your Workflow Win:**
```
Tableau/Power BI: GUI → GUI → GUI → Manual → Repeat
Metabase/Superset: SQL → Auto-Chart → API → Automate → Scale
```

**Perfect for CLI-loving developers who want BI capabilities!** 🎯🤖

**Ready to try Metabase? It's way more your speed than Tableau/Power BI!** 🚀
