#!/bin/bash
# Marketing Analytics ETL Pipeline Runner

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════╗"
echo "║  Marketing Analytics Dashboard - ETL Pipeline   ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: .env file not found"
    echo "   Using defaults (demo mode)"
fi

# Step 1: Extract
echo ""
echo "┌──────────────────────────────────────────────┐"
echo "│ STEP 1: EXTRACT (TheCocktailDB → Ad Campaigns)│"
echo "└──────────────────────────────────────────────┘"
python3 etl/fetch_from_cocktaildb.py

# Step 2: Transform
echo ""
echo "┌──────────────────────────────────────────────┐"
echo "│ STEP 2: TRANSFORM (Clean & Merge)            │"
echo "└──────────────────────────────────────────────┘"
python3 etl/clean_merge.py

# Step 3: Load
echo ""
echo "┌──────────────────────────────────────────────┐"
echo "│ STEP 3: LOAD (DuckDB)                        │"
echo "└──────────────────────────────────────────────┘"
python3 etl/load_to_duckdb.py

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     Pipeline Complete! ✅                        ║"
echo "║                                                  ║"
echo "║  Next Steps:                                     ║"
echo "║  1. Review data in db/ads_analytics.duckdb       ║"
echo "║  2. Run dashboard: streamlit run dashboard/app.py║"
echo "║  3. Schedule regular pipeline runs               ║"
echo "╚══════════════════════════════════════════════════╝"
