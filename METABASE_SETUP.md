# 🆓 Metabase Setup Guide (FREE & CLI-Friendly)

## Why Metabase is PERFECT for Your Budget & Preferences

### **Cost: $0 (Completely Free)**
```
✅ Open Source: No licensing fees ever
✅ Self-hosted: Your own infrastructure
✅ No user limits: Scale as needed
✅ No feature restrictions: Full functionality
```

### **CLI-Friendly: 80% SQL, 20% GUI**
```
Your Workflow (Minimal GUI!):
1. Write SQL queries (your strength)
2. Metabase auto-creates visualizations
3. Click "Add to dashboard" (2 clicks)
4. Done! Professional BI dashboard
```

---

## 🚀 Quick Metabase Setup (5 Minutes)

### **Step 1: Install with Docker (CLI!)**
```bash
# Pull and run Metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase

# Check it's running
docker ps | grep metabase

# Access at: http://localhost:3000
```

### **Step 2: First-Time Setup (2 Minutes)**
```
1. Open browser: http://localhost:3000
2. Create admin account
3. Skip tutorial (optional)
4. You're ready!
```

### **Step 3: Connect Your Data**
```bash
# Your CSV is ready - just connect!
ls marketing_data_for_bi.csv  # ✅ 1,620 rows of data
```

**In Metabase:**
```
1. Settings → Admin → Databases → Add database
2. Database type: CSV upload
3. Upload: marketing_data_for_bi.csv
4. Name: "Marketing Analytics Data"
5. Save
```

---

## 📊 Build Your First Dashboard (10 Minutes)

### **Step 1: Write Your First SQL Query**
```
-- Click "New" → "SQL Query"
-- Select your database
-- Paste this SQL:

SELECT 
    campaign_name,
    SUM(revenue) as total_revenue,
    SUM(cost) as total_cost,
    ROUND(SUM(revenue)/SUM(cost), 2) as roas,
    ROUND(AVG(ctr), 2) as avg_ctr,
    SUM(clicks) as total_clicks
FROM marketing_data_for_bi
GROUP BY campaign_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Click "Run query"
-- Metabase shows: Table + Auto-suggestions for charts
```

### **Step 2: Create Visualization (2 Clicks)**
```
1. Click "Visualize" button
2. Metabase suggests: Bar chart (revenue by campaign)
3. Click "Save" → Name: "Campaign Performance"
```

### **Step 3: Add to Dashboard**
```
1. Click "Add to dashboard"
2. Create new dashboard: "Marketing Analytics"
3. Add title: "Campaign Performance Overview"
4. Save
```

### **Step 4: Add More Charts (Repeat SQL Pattern)**
```sql
-- Time series trend
SELECT 
    DATE(date) as date,
    SUM(revenue) as daily_revenue,
    SUM(cost) as daily_cost
FROM marketing_data_for_bi
GROUP BY date
ORDER BY date;

-- Platform comparison  
SELECT 
    platform,
    SUM(revenue) as revenue,
    SUM(cost) as cost,
    ROUND(SUM(revenue)/SUM(cost), 2) as roas
FROM marketing_data_for_bi
GROUP BY platform;

-- Top products
SELECT 
    product_name,
    SUM(revenue) as revenue,
    SUM(orders) as orders,
    ROUND(AVG(gross_margin), 2) as avg_margin
FROM marketing_data_for_bi
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 5;
```

---

## 🎨 Dashboard Styling (Minimal GUI)

### **Make It Look Professional**
```
1. Dashboard settings → Change theme colors
2. Resize charts: Drag corners (minimal GUI work)
3. Add text cards: "Key Metrics Summary"
4. Reorder: Drag charts to preferred layout
5. Add filters: Date range, campaign selectors
```

### **Advanced: Custom CSS (Optional)**
```css
/* Add custom CSS in Admin → Settings → Appearance */
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
}
```

---

## 🤖 Automation & CLI Features

### **API Automation (For Later)**
```bash
# Get session token
TOKEN=$(curl -X POST "http://localhost:3000/api/session" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}' \
  | jq -r '.id')

# Create automated reports
curl -X POST "http://localhost:3000/api/card" \
  -H "X-Metabase-Session: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Revenue Report",
    "dataset_query": {
      "type": "native",
      "native": {
        "query": "SELECT SUM(revenue) FROM marketing_data_for_bi WHERE date = CURRENT_DATE"
      },
      "database": 1
    }
  }'
```

### **Scheduled Refreshes**
```bash
# Cron job for daily data refresh
0 6 * * * /path/to/refresh_metabase_data.sh

# Script content:
#!/bin/bash
# Update CSV data
python generate_fresh_data.py > marketing_data_for_bi.csv

# Trigger Metabase refresh
curl -X POST "http://localhost:3000/api/database/1/sync" \
  -H "X-Metabase-Session: $TOKEN"
```

---

## 💼 Portfolio & Resume Impact

### **Add to Your Resume:**
```
Business Intelligence & Analytics:
- Metabase: SQL-driven business intelligence dashboards
- Custom dashboard development with automated data pipelines
- Self-hosted BI infrastructure deployment
- API-based report automation and scheduling
```

### **Skills Demonstrated:**
```
✅ SQL query optimization for analytics
✅ Docker containerization and deployment  
✅ API integration and automation
✅ Business intelligence dashboard design
✅ Self-hosted infrastructure management
✅ Data visualization best practices
```

---

## 🔄 Migration Path (Future Growth)

### **Start Here (Free):**
```
✅ Metabase Open Source - Perfect foundation
✅ Docker deployment - Infrastructure as code
✅ SQL-first approach - Your strength
✅ Basic automation - API endpoints available
```

### **Scale Up (Still Free):**
```
✅ Apache Superset - More enterprise features
✅ Custom Python dashboards - Full control
✅ Kubernetes deployment - Production-ready
✅ Advanced automation - Python SDK
```

### **Enterprise (If Budget Allows):**
```
✅ Preset.io - Managed Superset ($)
✅ Custom internal tools - Like Airbnb/Meta
✅ Cloud data warehouses - BigQuery, Snowflake
```

---

## 🚀 Why Metabase > Paid Alternatives

### **Cost Comparison:**
```
Metabase Open Source: $0 forever
Tableau Public: $0 but limited & cloud-only
Power BI Free: $0 but very limited features
Superset: $0 (same as Metabase)

Tableau Creator: $70/month
Power BI Pro: $10/month  
Looker: $100+/month
```

### **Feature Comparison:**
```
Metabase: 90% of enterprise features, free
- SQL editor with autocomplete
- Advanced permissions & user management  
- Dashboard subscriptions & alerts
- API for automation
- White-labeling options
- Mobile-responsive dashboards
- Data sandboxing & row-level security
```

### **Your Workflow Fit:**
```
Metabase: 80% SQL writing, 20% light GUI
Perfect for CLI-loving developers!

vs.

Tableau: 90% GUI, 10% SQL
Power BI: 85% GUI, 15% DAX/formulas

Metabase matches your preferences perfectly!
```

---

## 🎯 Quick Decision Framework

### **Choose Metabase If:**
```
✅ You love writing SQL
✅ You hate GUI drag-and-drop work
✅ You want free, open-source tools
✅ You need self-hosted control
✅ You want API automation potential
✅ You prefer Docker/Kubernetes deployment
```

### **Budget Reality Check:**
```
Your Situation:
- No paid tool budget ✅
- CLI-heavy preferences ✅  
- SQL expertise ✅
- Docker comfort ✅

Metabase: Perfect match! 🎯
```

---

## 🚀 Get Started NOW (3 Commands)

```bash
# 1. Install Metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase

# 2. Check it's running
curl http://localhost:3000  # Should return HTML

# 3. Open in browser
open http://localhost:3000

# 4. Upload your data
# marketing_data_for_bi.csv is ready!

# 5. Start writing SQL queries!
```

**Result: Professional BI dashboard in 15 minutes, $0 cost, 80% CLI work!** 🎉

**Metabase is the BI tool that actually fits your budget and workflow!** 🚀🤖

**Ready to build your first SQL-powered dashboard?** 📊✨
