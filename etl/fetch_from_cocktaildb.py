#!/usr/bin/env python3
"""
TheCocktailDB API Fetcher for Marketing Campaigns

Fetches real cocktail/mocktail data from TheCocktailDB API (same as sibling projects)
and generates realistic Google Ads & Facebook Ads campaigns around them.
"""

import os
import sys
import requests
import random
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# TheCocktailDB API (free, no key needed - same as 02_mocktailverse & 03_cocktailverse)
COCKTAIL_API_BASE = "https://www.thecocktaildb.com/api/json/v1/1"


def fetch_cocktails_from_api(fetch_type: str = "all", limit: int = 20) -> List[Dict]:
    """
    Fetch cocktails from TheCocktailDB API
    
    Args:
        fetch_type: "all", "cocktails", "mocktails" (non-alcoholic)
        limit: Maximum number of drinks to fetch
        
    Returns:
        List of cocktail dictionaries
    """
    cocktails = []
    
    try:
        if fetch_type == "mocktails" or fetch_type == "non_alcoholic":
            # Fetch non-alcoholic drinks
            response = requests.get(f"{COCKTAIL_API_BASE}/filter.php?a=Non_Alcoholic", timeout=10)
            if response.status_code == 200:
                data = response.json()
                drinks = data.get("drinks", [])[:limit]
                
                # Get details for each drink
                for drink in drinks:
                    detail_response = requests.get(
                        f"{COCKTAIL_API_BASE}/lookup.php?i={drink['idDrink']}",
                        timeout=10
                    )
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        if detail_data.get("drinks"):
                            cocktails.append(detail_data["drinks"][0])
        
        elif fetch_type == "cocktails" or fetch_type == "alcoholic":
            # Fetch random cocktails
            for _ in range(min(limit, 20)):  # API limits
                response = requests.get(f"{COCKTAIL_API_BASE}/random.php", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("drinks"):
                        cocktails.append(data["drinks"][0])
        
        else:  # "all" - mix of both
            # Get some mocktails
            mocktail_response = requests.get(f"{COCKTAIL_API_BASE}/filter.php?a=Non_Alcoholic", timeout=10)
            if mocktail_response.status_code == 200:
                mocktail_data = mocktail_response.json()
                mocktail_drinks = mocktail_data.get("drinks", [])[:limit//2]
                for drink in mocktail_drinks:
                    detail_response = requests.get(
                        f"{COCKTAIL_API_BASE}/lookup.php?i={drink['idDrink']}",
                        timeout=10
                    )
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        if detail_data.get("drinks"):
                            cocktails.append(detail_data["drinks"][0])
            
            # Get some cocktails
            for _ in range(min(limit//2, 10)):
                response = requests.get(f"{COCKTAIL_API_BASE}/random.php", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("drinks"):
                        cocktails.append(data["drinks"][0])
        
        return cocktails[:limit]
        
    except Exception as e:
        print(f"⚠️  Error fetching from TheCocktailDB API: {e}")
        return []


def create_campaign_from_cocktail(cocktail: Dict, platform: str, days: int = 30) -> List[Dict]:
    """
    Create realistic ad campaign data from a real cocktail
    
    Args:
        cocktail: Cocktail data from TheCocktailDB API
        platform: "google_ads" or "facebook_ads"
        days: Number of days of campaign data
        
    Returns:
        List of daily campaign records
    """
    drink_name = cocktail.get("strDrink", "Unknown Drink")
    drink_category = cocktail.get("strCategory", "Cocktail")
    is_alcoholic = cocktail.get("strAlcoholic", "Alcoholic") == "Alcoholic"
    
    # Create campaign name based on real drink
    if is_alcoholic:
        campaign_name = f"{drink_name} - Premium Cocktail Campaign"
    else:
        campaign_name = f"{drink_name} - Refreshing Mocktail Campaign"
    
    campaign_id = f"{platform}_campaign_{cocktail.get('idDrink', random.randint(1000, 9999))}"
    
    base_date = datetime.now()
    data = []
    
    # Base performance metrics (alcoholic drinks typically perform better)
    if is_alcoholic:
        base_impressions = random.randint(5000, 80000)
        base_ctr = random.uniform(0.025, 0.12)  # 2.5-12% CTR
        base_conversion = random.uniform(0.04, 0.22)  # 4-22% conversion
        base_cpc = random.uniform(0.90, 3.80)  # Higher CPC
        roas_multiplier = random.uniform(2.2, 6.5)  # Better ROAS
    else:
        base_impressions = random.randint(3000, 50000)
        base_ctr = random.uniform(0.018, 0.10)  # 1.8-10% CTR
        base_conversion = random.uniform(0.025, 0.18)  # 2.5-18% conversion
        base_cpc = random.uniform(0.55, 2.80)  # Lower CPC
        roas_multiplier = random.uniform(1.6, 4.8)  # Good ROAS
    
    # Popular drinks get better performance
    if drink_category in ["Cocktail", "Ordinary Drink", "Shot"]:
        base_impressions = int(base_impressions * 1.2)
        base_ctr *= 1.15
    
    for day in range(days):
        date = base_date - timedelta(days=days - day - 1)
        
        # Weekend/weekday variation
        weekday = date.weekday()
        if weekday >= 5:  # Weekend
            impressions = int(base_impressions * random.uniform(1.25, 1.55))
        else:
            impressions = int(base_impressions * random.uniform(0.85, 1.15))
        
        clicks = int(impressions * base_ctr)
        conversions = int(clicks * base_conversion)
        cost = round(clicks * base_cpc, 2)
        revenue = round(cost * roas_multiplier, 2)
        
        # Seasonal trends (summer months perform better for drinks)
        month = date.month
        if month in [6, 7, 8]:  # Summer
            impressions = int(impressions * 1.35)
            clicks = int(clicks * 1.35)
            conversions = int(conversions * 1.25)
            cost = round(cost * 1.35, 2)
            revenue = round(revenue * 1.25, 2)
        
        data.append({
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "date": date.strftime("%Y-%m-%d"),
            "platform": platform,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "cost": cost,
            "revenue": revenue,
            # Additional metadata from TheCocktailDB
            "drink_id": cocktail.get("idDrink"),
            "drink_category": drink_category,
            "is_alcoholic": is_alcoholic
        })
    
    return data


def generate_ads_from_cocktaildb(platform: str, num_campaigns: int = 10, days: int = 30) -> List[Dict]:
    """
    Generate ad campaigns from real TheCocktailDB data
    
    Args:
        platform: "google_ads" or "facebook_ads"
        num_campaigns: Number of campaigns (drinks) to create
        days: Number of days of data per campaign
        
    Returns:
        List of campaign records
    """
    print(f"🍹 Fetching real cocktails from TheCocktailDB API...")
    print(f"   (Same API used in 02_mocktailverse & 03_cocktailverse)")
    
    # Fetch cocktails (mix of alcoholic and non-alcoholic)
    cocktails = fetch_cocktails_from_api(fetch_type="all", limit=num_campaigns)
    
    if not cocktails:
        print("⚠️  No cocktails fetched. Using fallback data...")
        return []
    
    print(f"✅ Fetched {len(cocktails)} real cocktails from TheCocktailDB")
    
    # Create campaigns from real cocktails
    all_campaigns = []
    for cocktail in cocktails:
        campaign_data = create_campaign_from_cocktail(cocktail, platform, days)
        all_campaigns.extend(campaign_data)
    
    return all_campaigns


def main():
    """Main function"""
    print("🍹 TheCocktailDB → Marketing Ads Data Generator")
    print("   Using real cocktail data (same as sibling projects)")
    print("")
    
    # Generate Google Ads data
    print("📦 Generating Google Ads campaigns from real cocktails...")
    google_ads_data = generate_ads_from_cocktaildb("google_ads", num_campaigns=10, days=30)
    
    if google_ads_data:
        output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
        os.makedirs(output_dir, exist_ok=True)
        
        google_ads_path = os.path.join(output_dir, "google_ads.csv")
        df = pd.DataFrame(google_ads_data)
        # Remove metadata columns for final output (keep only standard schema)
        df_output = df[["campaign_id", "campaign_name", "date", "platform", 
                       "impressions", "clicks", "conversions", "cost", "revenue"]]
        df_output.to_csv(google_ads_path, index=False)
        print(f"✅ Saved: {google_ads_path} ({len(df_output)} rows)")
        print(f"   - Real cocktails used: {df['drink_id'].nunique()}")
    
    # Generate Facebook Ads data
    print("\n📦 Generating Facebook Ads campaigns from real cocktails...")
    facebook_ads_data = generate_ads_from_cocktaildb("facebook_ads", num_campaigns=10, days=30)
    
    if facebook_ads_data:
        facebook_ads_path = os.path.join(output_dir, "facebook_ads.csv")
        df = pd.DataFrame(facebook_ads_data)
        df_output = df[["campaign_id", "campaign_name", "date", "platform", 
                       "impressions", "clicks", "conversions", "cost", "revenue"]]
        df_output.to_csv(facebook_ads_path, index=False)
        print(f"✅ Saved: {facebook_ads_path} ({len(df_output)} rows)")
        print(f"   - Real cocktails used: {df['drink_id'].nunique()}")
    
    print("\n🎉 Real cocktail-based ad campaigns generated!")
    print("   Data sourced from TheCocktailDB (same as 02_mocktailverse & 03_cocktailverse)")


if __name__ == "__main__":
    main()

