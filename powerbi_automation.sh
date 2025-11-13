#!/bin/bash
# Power BI Service Automation using REST API

# Requires: Power BI Pro license + Azure App Registration

CLIENT_ID="your-app-id"
CLIENT_SECRET="your-secret"  
TENANT_ID="your-tenant"

# Get access token
TOKEN=$(curl -X POST "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID&scope=https://analysis.windows.net/powerbi/api/.default&client_secret=$CLIENT_SECRET&grant_type=client_credentials" \
  | jq -r '.access_token')

# Publish PBIX file
curl -X POST "https://api.powerbi.com/v1.0/myorg/groups/$GROUP_ID/imports" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "fileInput=@marketing_dashboard.pbix"

echo "Power BI dashboard published to service"
