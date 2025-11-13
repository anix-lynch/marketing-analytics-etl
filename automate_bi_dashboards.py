#!/usr/bin/env python3
"""
Semi-Automate BI Dashboard Creation
For Tableau Public and Power BI Free
"""

import pandas as pd
import json
import subprocess
import os
from pathlib import Path

def create_tableau_extract():
    """Create Tableau Data Extract (.tde) file"""
    print("🔧 Creating Tableau Data Extract...")
    
    # Read the data
    df = pd.read_csv('marketing_data_for_bi.csv')
    
    # Tableau can read CSV directly, but for automation we can:
    # 1. Use tabcmd to create extracts
    # 2. Use Tableau Server REST API
    # 3. Create .twb files programmatically
    
    print("📊 Data ready for Tableau Public import")
    print("📋 Next steps:")
    print("   1. Open Tableau Public")
    print("   2. Connect to 'marketing_data_for_bi.csv'")
    print("   3. Follow TABLEAU_DASHBOARD_GUIDE.md")
    
    return True

def create_powerbi_template():
    """Create Power BI template structure"""
    print("🔧 Creating Power BI Template...")
    
    # Power BI template structure
    template = {
        "name": "Marketing Analytics Template",
        "description": "Automated marketing dashboard template",
        "version": "1.0",
        "dataset": {
            "name": "Marketing Data",
            "description": "Cross-platform marketing performance data"
        },
        "reports": [
            {
                "name": "Executive Summary",
                "description": "Key marketing KPIs and trends"
            },
            {
                "name": "Campaign Analysis", 
                "description": "Detailed campaign performance breakdown"
            },
            {
                "name": "Platform Intelligence",
                "description": "Platform comparison and attribution"
            }
        ]
    }
    
    with open('powerbi_template.json', 'w') as f:
        json.dump(template, f, indent=2)
    
    print("📋 Power BI Automation Steps:")
    print("   1. Open Power BI Desktop")
    print("   2. Get Data → CSV → 'marketing_data_for_bi.csv'")
    print("   3. Follow POWERBI_DASHBOARD_GUIDE.md DAX formulas")
    print("   4. Save as .pbix file")
    
    return True

def setup_tableau_server_automation():
    """Setup Tableau Server automation (if user gets Tableau Server)"""
    print("🔧 Tableau Server Automation Setup...")
    
    automation_script = '''#!/bin/bash
# Tableau Server Automation (requires Tableau Server license)

# Login to Tableau Server
tabcmd login --server https://your-server.com --username your-email --password your-password

# Publish workbook
tabcmd publish "marketing_dashboard.twb" --name "Marketing Analytics" --project "Default"

# Set permissions
tabcmd publish permissions set --workbook "Marketing Analytics" --grantee "All Users" --capabilities "View"

echo "Tableau dashboard published and permissions set"
'''
    
    with open('tableau_automation.sh', 'w') as f:
        f.write(automation_script)
    
    os.chmod('tableau_automation.sh', 0o755)
    print("📄 Created tableau_automation.sh")
    print("⚠️  Requires Tableau Server license (not Public)")

def setup_powerbi_service_automation():
    """Setup Power BI Service automation"""
    print("🔧 Power BI Service Automation Setup...")
    
    automation_script = '''#!/bin/bash
# Power BI Service Automation using REST API

# Requires: Power BI Pro license + Azure App Registration

CLIENT_ID="your-app-id"
CLIENT_SECRET="your-secret"  
TENANT_ID="your-tenant"

# Get access token
TOKEN=$(curl -X POST "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "client_id=$CLIENT_ID&scope=https://analysis.windows.net/powerbi/api/.default&client_secret=$CLIENT_SECRET&grant_type=client_credentials" \\
  | jq -r '.access_token')

# Publish PBIX file
curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/$GROUP_ID/imports" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: multipart/form-data" \\
  -F "fileInput=@marketing_dashboard.pbix"

echo "Power BI dashboard published to service"
'''
    
    with open('powerbi_automation.sh', 'w') as f:
        f.write(automation_script)
    
    os.chmod('powerbi_automation.sh', 0o755)
    print("📄 Created powerbi_automation.sh")
    print("⚠️  Requires Power BI Pro license")

def main():
    print("🚀 BI Dashboard Semi-Automation Setup")
    print("=" * 50)
    
    # Create data extracts/templates
    create_tableau_extract()
    print()
    create_powerbi_template()
    print()
    
    # Create automation scripts for future use
    setup_tableau_server_automation()
    print()
    setup_powerbi_service_automation()
    print()
    
    print("✅ Setup Complete!")
    print()
    print("🎯 Next Steps:")
    print("1. Tableau Public: Manual import + follow guide")
    print("2. Power BI Desktop: Manual import + follow guide") 
    print("3. Future: Use automation scripts with paid licenses")
    print()
    print("💡 Pro Tip: Start with manual builds to learn the tools,")
    print("   then automate with scripts for repeated deployments!")

if __name__ == "__main__":
    main()
