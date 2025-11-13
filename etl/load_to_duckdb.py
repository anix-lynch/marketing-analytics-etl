#!/usr/bin/env python3
"""
DuckDB Data Loader

Loads unified CSV data into DuckDB for analytics.
Creates db/ads_analytics.duckdb
"""

import os
import duckdb
import pandas as pd


def load_to_duckdb(csv_path: str, db_path: str, table_name: str = "ads_analytics"):
    """
    Load CSV data into DuckDB
    
    Args:
        csv_path: Path to unified CSV file
        db_path: Path to DuckDB file
        table_name: Name of the table
    """
    print(f"📦 Loading data into DuckDB: {db_path}")
    
    # Create database directory if needed
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to DuckDB
    conn = duckdb.connect(db_path)
    
    # Read CSV
    print(f"   Reading {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Create table (replace if exists)
    print(f"   Creating table '{table_name}'...")
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Insert data
    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    
    # Create indexes for better query performance
    print("   Creating indexes...")
    try:
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_date ON {table_name}(date)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_platform ON {table_name}(platform)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_campaign ON {table_name}(campaign_id)")
    except Exception as e:
        print(f"   Note: Index creation: {e}")
    
    # Get table info
    result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
    row_count = result[0] if result else 0
    
    result = conn.execute(f"SELECT COUNT(DISTINCT campaign_id) FROM {table_name}").fetchone()
    campaign_count = result[0] if result else 0
    
    result = conn.execute(f"SELECT COUNT(DISTINCT platform) FROM {table_name}").fetchone()
    platform_count = result[0] if result else 0
    
    conn.close()
    
    print(f"✅ Data loaded successfully!")
    print(f"   - Rows: {row_count}")
    print(f"   - Campaigns: {campaign_count}")
    print(f"   - Platforms: {platform_count}")
    print(f"   - Database: {db_path}")


def main():
    """Main loading function"""
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, "..", "data", "clean", "unified_ads.csv")
    db_path = os.path.join(script_dir, "..", "db", "ads_analytics.duckdb")
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found!")
        print("   Run clean_merge.py first.")
        return
    
    load_to_duckdb(csv_path, db_path)


if __name__ == "__main__":
    main()

