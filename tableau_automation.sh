#!/bin/bash
# Tableau Server Automation (requires Tableau Server license)

# Login to Tableau Server
tabcmd login --server https://your-server.com --username your-email --password your-password

# Publish workbook
tabcmd publish "marketing_dashboard.twb" --name "Marketing Analytics" --project "Default"

# Set permissions
tabcmd publish permissions set --workbook "Marketing Analytics" --grantee "All Users" --capabilities "View"

echo "Tableau dashboard published and permissions set"
