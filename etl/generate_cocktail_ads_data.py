#!/usr/bin/env python3
"""
Cocktail/Mocktail Themed Ads Data Generator

Generates realistic Google Ads & Facebook Ads data for cocktail/mocktail campaigns.
Aligns with sibling projects: 02_mocktailverse and 03_cocktailverse.
"""

import os
import random
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict


# Cocktail/Mocktail themed campaigns
COCKTAIL_CAMPAIGNS = [
    "Summer Cocktail Collection 2025",
    "Classic Martini Campaign",
    "Tropical Paradise Drinks",
    "Craft Cocktail Masterclass",
    "Premium Whiskey Selection",
    "Gin & Tonic Special",
    "Margarita Monday Promotion",
    "Old Fashioned Revival",
    "Craft Beer & Cocktail Pairing",
    "Holiday Cocktail Menu Launch"
]

MOCKTAIL_CAMPAIGNS = [
    "Refreshing Mocktail Collection",
    "Zero-Proof Summer Drinks",
    "Healthy Mocktail Alternatives",
    "Mocktail Mixology Workshop",
    "Non-Alcoholic Happy Hour",
    "Family-Friendly Drink Menu",
    "Wellness Mocktail Series",
    "Mocktail Recipe Book Launch",
    "Kids & Teens Mocktail Bar",
    "Sober October Mocktail Challenge"
]


def generate_cocktail_ads_data(platform: str, num_campaigns: int = 10, days: int = 30) -> List[Dict]:
    """
    Generate cocktail/mocktail themed ads data
    
    Args:
        platform: 'google_ads' or 'facebook_ads'
        num_campaigns: Number of campaigns
        days: Number of days of data
        
    Returns:
        List of campaign records
    """
    # Mix cocktail and mocktail campaigns
    all_campaigns = COCKTAIL_CAMPAIGNS + MOCKTAIL_CAMPAIGNS
    selected_campaigns = random.sample(all_campaigns, min(num_campaigns, len(all_campaigns)))
    
    base_date = datetime.now()
    data = []
    
    for i, campaign_name in enumerate(selected_campaigns):
        campaign_id = f"{platform}_campaign_{i+1}_{random.randint(1000, 9999)}"
        
        # Determine if cocktail or mocktail (affects performance)
        is_cocktail = campaign_name in COCKTAIL_CAMPAIGNS
        
        for day in range(days):
            date = base_date - timedelta(days=days - day - 1)
            
            # Cocktail campaigns typically have higher engagement
            if is_cocktail:
                base_impressions = random.randint(5000, 80000)
                base_ctr = random.uniform(0.02, 0.12)  # 2-12% CTR
                base_conversion = random.uniform(0.03, 0.20)  # 3-20% conversion
                base_cpc = random.uniform(0.80, 3.50)  # Higher CPC for cocktails
                roas_multiplier = random.uniform(2.0, 6.0)  # Better ROAS
            else:
                base_impressions = random.randint(3000, 50000)
                base_ctr = random.uniform(0.015, 0.10)  # 1.5-10% CTR
                base_conversion = random.uniform(0.02, 0.15)  # 2-15% conversion
                base_cpc = random.uniform(0.50, 2.50)  # Lower CPC for mocktails
                roas_multiplier = random.uniform(1.5, 4.5)  # Good but lower ROAS
            
            # Add weekend/weekday variation
            weekday = date.weekday()
            if weekday >= 5:  # Weekend
                impressions = int(base_impressions * random.uniform(1.2, 1.5))
            else:
                impressions = int(base_impressions * random.uniform(0.8, 1.2))
            
            clicks = int(impressions * base_ctr)
            conversions = int(clicks * base_conversion)
            cost = round(clicks * base_cpc, 2)
            revenue = round(cost * roas_multiplier, 2)
            
            # Add some seasonal trends (summer months perform better)
            month = date.month
            if month in [6, 7, 8]:  # Summer
                impressions = int(impressions * 1.3)
                clicks = int(clicks * 1.3)
                conversions = int(conversions * 1.2)
                cost = round(cost * 1.3, 2)
                revenue = round(revenue * 1.2, 2)
            
            data.append({
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "date": date.strftime("%Y-%m-%d"),
                "platform": platform,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "cost": cost,
                "revenue": revenue
            })
    
    return data


def generate_google_ads_cocktail_data(num_campaigns: int = 10, days: int = 30) -> List[Dict]:
    """Generate Google Ads data for cocktail/mocktail campaigns"""
    return generate_cocktail_ads_data("google_ads", num_campaigns, days)


def generate_facebook_ads_cocktail_data(num_campaigns: int = 10, days: int = 30) -> List[Dict]:
    """Generate Facebook Ads data for cocktail/mocktail campaigns"""
    return generate_cocktail_ads_data("facebook_ads", num_campaigns, days)


def main():
    """Generate cocktail/mocktail themed ads data"""
    print("🍹 Generating Cocktail/Mocktail Themed Ads Data...")
    print("   Aligned with 02_mocktailverse & 03_cocktailverse projects")
    print("")
    
    # Generate Google Ads data
    print("📦 Generating Google Ads data (cocktail/mocktail campaigns)...")
    google_ads_data = generate_google_ads_cocktail_data(num_campaigns=10, days=30)
    
    # Save to data/raw/
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    google_ads_path = os.path.join(output_dir, "google_ads.csv")
    pd.DataFrame(google_ads_data).to_csv(google_ads_path, index=False)
    print(f"✅ Saved: {google_ads_path} ({len(google_ads_data)} rows)")
    
    # Generate Facebook Ads data
    print("📦 Generating Facebook Ads data (cocktail/mocktail campaigns)...")
    facebook_ads_data = generate_facebook_ads_cocktail_data(num_campaigns=10, days=30)
    
    facebook_ads_path = os.path.join(output_dir, "facebook_ads.csv")
    pd.DataFrame(facebook_ads_data).to_csv(facebook_ads_path, index=False)
    print(f"✅ Saved: {facebook_ads_path} ({len(facebook_ads_data)} rows)")
    
    # Summary
    print("")
    print("📊 Campaign Summary:")
    google_df = pd.DataFrame(google_ads_data)
    facebook_df = pd.DataFrame(facebook_ads_data)
    
    print(f"   Google Ads:")
    print(f"     - Campaigns: {google_df['campaign_name'].nunique()}")
    print(f"     - Total Cost: ${google_df['cost'].sum():,.2f}")
    print(f"     - Total Revenue: ${google_df['revenue'].sum():,.2f}")
    print(f"     - Avg ROAS: {google_df['revenue'].sum() / google_df['cost'].sum():.2f}x")
    
    print(f"   Facebook Ads:")
    print(f"     - Campaigns: {facebook_df['campaign_name'].nunique()}")
    print(f"     - Total Cost: ${facebook_df['cost'].sum():,.2f}")
    print(f"     - Total Revenue: ${facebook_df['revenue'].sum():,.2f}")
    print(f"     - Avg ROAS: {facebook_df['revenue'].sum() / facebook_df['cost'].sum():.2f}x")
    
    print("")
    print("🎉 Cocktail/Mocktail ads data generated!")
    print("   Ready to run: ./run_pipeline.sh")


if __name__ == "__main__":
    main()

