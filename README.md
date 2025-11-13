# Marketing Analytics Dashboard – Google & Facebook ETL

A complete ETL pipeline that ingests marketing data from Google Ads and Facebook Ads, transforms it, and visualizes KPIs like impressions, CTR, conversions, and ROAS.

## Pipeline Overview

```
┌──────────────────────────────────────────────┐
│           EXTRACT (API or Demo)              │
│──────────────────────────────────────────────│
│  📦 Google Ads API → google_ads.csv          │
│  📦 Facebook Ads API → facebook_ads.csv      │
│  📦 Demo mode available for learning        │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│         TRANSFORM (Clean & Merge)            │
│──────────────────────────────────────────────│
│  🧮 Normalize campaign_id, timestamps        │
│  📊 Compute CTR, CPC, ROAS                  │
│  🗃️ Output unified_ads.csv                  │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│             LOAD (DuckDB)                    │
│──────────────────────────────────────────────│
│  🗄️ Store in ads_analytics.duckdb            │
│  🪄 Ready for analytics queries               │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│         VISUALIZE (Streamlit)                │
│──────────────────────────────────────────────│
│  📊 Dashboard:                               │
│    - KPIs: CTR, ROAS, CPC                    │
│    - Time series trends                      │
│    - Campaign breakdown                      │
│    - Platform comparison                      │
└──────────────────────────────────────────────┘
```

## Directory Structure

```
marketing-etl/
├── etl/                      # ETL scripts
│   ├── fetch_google_ads.py   # Google Ads API connector
│   ├── fetch_facebook_ads.py # Facebook Ads API connector
│   ├── clean_merge.py        # Data cleaning & merging
│   ├── load_to_duckdb.py     # DuckDB loader
│   └── generate_demo_data.py # Demo data generator
├── dashboard/                # Streamlit dashboard
│   └── app.py               # Main dashboard app
├── db/                       # DuckDB database
│   └── ads_analytics.duckdb # Analytics database
├── data/
│   ├── raw/                  # Raw CSV from APIs
│   │   ├── google_ads.csv
│   │   └── facebook_ads.csv
│   └── clean/                # Processed data
│       └── unified_ads.csv
├── run_pipeline.sh           # CLI pipeline runner
├── requirements.txt          # Python dependencies
├── env.example              # Environment variables template
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Pipeline (Demo Mode - No API Keys Needed!)

```bash
./run_pipeline.sh
```

This will:
1. Fetch **real cocktails from TheCocktailDB API** (same as 02_mocktailverse & 03_cocktailverse)
2. Generate realistic ad campaigns around real drinks
3. Clean and merge datasets
4. Compute metrics (CTR, CPC, ROAS)
5. Load into DuckDB

### 3. Launch Dashboard

```bash
streamlit run dashboard/app.py
```

### 4. Optional: Use Real Data

See [DATA_SOURCES.md](DATA_SOURCES.md) for:
- Real API credentials (Google Ads, Facebook Ads)
- Hugging Face datasets
- Kaggle datasets

## Usage

### Demo Mode (No API Keys Needed)

By default, the pipeline runs in demo mode and generates realistic sample data. Perfect for:
- Learning the pipeline structure
- Testing the dashboard
- Portfolio demonstrations

Set `USE_DEMO_DATA=true` in `.env` or leave it unset.

### Production Mode (With API Keys)

1. **Google Ads API** (b-turn: Get credentials from [Google Ads API Center](https://ads.google.com/aw/apicenter))
   - `GOOGLE_ADS_CUSTOMER_ID`
   - `GOOGLE_ADS_DEVELOPER_TOKEN`
   - `GOOGLE_ADS_CLIENT_ID`
   - `GOOGLE_ADS_CLIENT_SECRET`
   - `GOOGLE_ADS_REFRESH_TOKEN`

2. **Facebook Ads API** (b-turn: Get credentials from [Facebook Developers](https://developers.facebook.com/))
   - `FACEBOOK_ADS_ACCESS_TOKEN`
   - `FACEBOOK_ADS_ACCOUNT_ID`

3. Set `USE_DEMO_DATA=false` in `.env`

4. Run pipeline: `./run_pipeline.sh`

## Metrics Computed

- **CTR (Click-Through Rate)**: `(Clicks / Impressions) * 100`
- **CPC (Cost Per Click)**: `Cost / Clicks`
- **ROAS (Return on Ad Spend)**: `Revenue / Cost`
- **Conversion Rate**: `(Conversions / Clicks) * 100`

## Dashboard Features

- **KPIs**: Total cost, revenue, clicks, conversions, impressions, CTR, ROAS, CPC
- **Time Series**: Trend analysis over time with platform comparison
- **Campaign Breakdown**: Top campaigns by various metrics
- **Platform Comparison**: Side-by-side Google Ads vs Facebook Ads
- **Filters**: Date range, platform, campaign selection

## CLI Workflow

```bash
# Full pipeline
./run_pipeline.sh

# Individual steps
python3 etl/fetch_google_ads.py
python3 etl/fetch_facebook_ads.py
python3 etl/clean_merge.py
python3 etl/load_to_duckdb.py
streamlit run dashboard/app.py
```

## Design Principles

- **Local-first**: DuckDB file-based database, no cloud dependencies
- **CLI reproducible**: Single script runs entire pipeline
- **Demo-friendly**: Works without API keys
- **Clean ETL structure**: Clear separation of extract, transform, load
- **Simple visualization**: Streamlit dashboard with Plotly charts

## Requirements

- Python 3.8+
- DuckDB (included in requirements.txt)
- Streamlit (included in requirements.txt)
- Plotly (included in requirements.txt)

## Next Steps

1. ✅ Run pipeline with demo data
2. 📊 Explore dashboard visualizations
3. 🔑 Add API credentials for real data
4. ⏰ Schedule regular pipeline runs (cron, GitHub Actions, etc.)
5. 📈 Customize dashboard for your needs

## License

MIT
