#!/bin/bash
# Complete Tableau CLI Workflow (Manual → Semi-Auto → Full Auto)

echo "=== TABLEAU CLI WORKFLOW ==="
echo

# PHASE 1: Manual Setup (What you do now)
echo "📋 PHASE 1: MANUAL (Current)"
echo "   1. Open Tableau Public GUI"
echo "   2. File → Open → marketing_data_for_bi.csv"  
echo "   3. Drag dimensions/measures manually"
echo "   4. Create each visualization by hand"
echo "   5. Arrange dashboard layout manually"
echo "   6. File → Save to Tableau Public"
echo "⏱️  Time: 2-4 hours per dashboard"
echo

# PHASE 2: Semi-Automation (With Scripts)
echo "🤖 PHASE 2: SEMI-AUTOMATION (With tableau_automation.sh)"
echo "   1. Build dashboard manually once (save as .twb)"
echo "   2. Run: ./tableau_cli_workflow.sh"
echo "   3. Script publishes to Tableau Server automatically"
echo "   4. Sets permissions and sharing automatically"
echo "⏱️  Time: 10 minutes + initial build time"
echo

# PHASE 3: Full Automation (Future)
echo "🚀 PHASE 3: FULL AUTOMATION (Tableau Server + API)"
echo "   1. Data updates automatically"
echo "   2. Dashboard refreshes via API calls"
echo "   3. Scheduled publishing via cron"
echo "   4. Email alerts for anomalies"
echo "⏱️  Time: 5 minutes (completely hands-off)"
echo

echo "=== CURRENT WORKFLOW (What you can do NOW) ==="
echo

# Check if Tableau is installed
if [ -d "/Applications/Tableau Public.app" ]; then
    echo "✅ Tableau Public installed"
else
    echo "❌ Install Tableau Public: https://public.tableau.com/s/"
    exit 1
fi

# Check data file
if [ -f "marketing_data_for_bi.csv" ]; then
    echo "✅ Data file ready: marketing_data_for_bi.csv"
else
    echo "❌ Run: python3 automate_bi_dashboards.py"
    exit 1
fi

echo
echo "🎯 MANUAL STEPS (CLI-friendly approach):"
echo
echo "1. Launch Tableau (CLI):"
echo "   open /Applications/Tableau\ Public.app"
echo
echo "2. Connect to data (in Tableau GUI):"
echo "   - File → Open → From File → Text File"
echo "   - Select: marketing_data_for_bi.csv"
echo "   - Click 'Connect'"
echo
echo "3. Build dashboard (follow guide):"
echo "   - Open TABLEAU_DASHBOARD_GUIDE.md"
echo "   - Follow step-by-step instructions"
echo "   - Use keyboard shortcuts where possible"
echo
echo "4. Save and publish:"
echo "   - File → Save to Tableau Public"
echo "   - Name: Marketing Analytics Dashboard"
echo "   - Description: Cross-platform marketing performance"
echo
echo "5. Get share link:"
echo "   - Copy URL from Tableau Public"
echo "   - Add to portfolio: gozeroshot.dev"
echo

echo "=== FUTURE AUTOMATION (When you get licenses) ==="
echo
echo "# Tableau Server Automation (requires license)"
echo "tabcmd login --server https://your-tableau-server.com"
echo "tabcmd publish marketing_dashboard.twb --name 'Marketing Analytics'"
echo "tabcmd set permissions --workbook 'Marketing Analytics' --allow-public true"
echo
echo "# Scheduled refreshes (cron job)"
echo "0 */6 * * * /path/to/refresh_tableau_data.sh  # Every 6 hours"
echo
echo "# API-driven updates"
echo "curl -X POST https://tableau-server/api/refresh-workbook \\"
echo "  -H 'Authorization: token' \\"
echo "  -d 'workbook_id=marketing-analytics'"
