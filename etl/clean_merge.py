#!/usr/bin/env python3
"""
Data Cleaning and Merging

Cleans and unifies Google Ads and Facebook Ads data.
Computes CTR, CPC, and ROAS metrics.
Outputs unified CSV to data/clean/unified_ads.csv
"""

import os
import pandas as pd
from typing import Optional


def normalize_campaign_id(campaign_id: str, platform: str) -> str:
    """
    Normalize campaign ID across platforms
    
    Args:
        campaign_id: Original campaign ID
        platform: Platform name (google_ads or facebook_ads)
        
    Returns:
        Normalized campaign ID
    """
    if pd.isna(campaign_id):
        return f"{platform}_unknown"
    
    # Ensure consistent format
    campaign_id = str(campaign_id).strip()
    if not campaign_id.startswith(platform):
        return f"{platform}_{campaign_id}"
    
    return campaign_id


def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute marketing metrics: CTR, CPC, ROAS
    
    Args:
        df: DataFrame with impressions, clicks, conversions, cost, revenue
        
    Returns:
        DataFrame with computed metrics
    """
    df = df.copy()
    
    # CTR: Click-Through Rate = (Clicks / Impressions) * 100
    df["ctr"] = (df["clicks"] / df["impressions"].replace(0, pd.NA) * 100).fillna(0).round(2)
    
    # CPC: Cost Per Click = Cost / Clicks
    df["cpc"] = (df["cost"] / df["clicks"].replace(0, pd.NA)).fillna(0).round(2)
    
    # ROAS: Return on Ad Spend = Revenue / Cost
    df["roas"] = (df["revenue"] / df["cost"].replace(0, pd.NA)).fillna(0).round(2)
    
    # Conversion Rate: Conversions / Clicks * 100
    df["conversion_rate"] = (df["conversions"] / df["clicks"].replace(0, pd.NA) * 100).fillna(0).round(2)
    
    return df


def clean_and_merge(raw_data_dir: str, output_dir: str) -> pd.DataFrame:
    """
    Clean and merge Google Ads and Facebook Ads data
    
    Args:
        raw_data_dir: Directory containing raw CSV files
        output_dir: Directory to save cleaned data
        
    Returns:
        Unified DataFrame
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Load raw data
    google_ads_path = os.path.join(raw_data_dir, "google_ads.csv")
    facebook_ads_path = os.path.join(raw_data_dir, "facebook_ads.csv")
    
    google_df = None
    facebook_df = None
    
    if os.path.exists(google_ads_path):
        print("📊 Loading Google Ads data...")
        google_df = pd.read_csv(google_ads_path)
        print(f"   - Rows: {len(google_df)}")
    else:
        print("⚠️  google_ads.csv not found")
    
    if os.path.exists(facebook_ads_path):
        print("📊 Loading Facebook Ads data...")
        facebook_df = pd.read_csv(facebook_ads_path)
        print(f"   - Rows: {len(facebook_df)}")
    else:
        print("⚠️  facebook_ads.csv not found")
    
    # Combine datasets
    if google_df is not None and facebook_df is not None:
        print("\n🔗 Merging datasets...")
        unified_df = pd.concat([google_df, facebook_df], ignore_index=True)
    elif google_df is not None:
        unified_df = google_df
    elif facebook_df is not None:
        unified_df = facebook_df
    else:
        raise ValueError("No data files found! Run fetch scripts first.")
    
    # Normalize campaign IDs
    print("🧹 Normalizing data...")
    unified_df["campaign_id"] = unified_df.apply(
        lambda row: normalize_campaign_id(row["campaign_id"], row["platform"]),
        axis=1
    )
    
    # Ensure numeric columns
    numeric_cols = ["impressions", "clicks", "conversions", "cost", "revenue"]
    for col in numeric_cols:
        if col in unified_df.columns:
            unified_df[col] = pd.to_numeric(unified_df[col], errors="coerce").fillna(0)
    
    # Ensure date column is datetime
    if "date" in unified_df.columns:
        unified_df["date"] = pd.to_datetime(unified_df["date"], errors="coerce")
        unified_df["date"] = unified_df["date"].dt.strftime("%Y-%m-%d")
    
    # Compute metrics
    print("📈 Computing metrics (CTR, CPC, ROAS)...")
    unified_df = compute_metrics(unified_df)
    
    # Sort by date and platform
    unified_df = unified_df.sort_values(["date", "platform", "campaign_id"], ascending=[False, True, True])
    
    # Reset index
    unified_df = unified_df.reset_index(drop=True)
    
    # Save unified data
    output_path = os.path.join(output_dir, "unified_ads.csv")
    unified_df.to_csv(output_path, index=False)
    
    print(f"\n✅ Unified data saved to {output_path}")
    print(f"   - Total rows: {len(unified_df)}")
    print(f"   - Campaigns: {unified_df['campaign_id'].nunique()}")
    print(f"   - Platforms: {', '.join(unified_df['platform'].unique())}")
    print(f"   - Date range: {unified_df['date'].min()} to {unified_df['date'].max()}")
    print(f"   - Metrics computed: CTR, CPC, ROAS, Conversion Rate")
    
    return unified_df


def main():
    """Main cleaning and merging function"""
    script_dir = os.path.dirname(__file__)
    raw_data_dir = os.path.join(script_dir, "..", "data", "raw")
    output_dir = os.path.join(script_dir, "..", "data", "clean")
    
    clean_and_merge(raw_data_dir, output_dir)
    print("\n✅ Clean and merge complete!")


if __name__ == "__main__":
    main()

