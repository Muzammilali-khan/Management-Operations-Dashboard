"""
Main Management Operations Dashboard
Run this file to execute the complete pipeline
"""

import os
import sys
from datetime import datetime

def run_pipeline():
    """Run complete management dashboard pipeline"""
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     MANAGEMENT OPERATIONS DASHBOARD                          ║
║     Complete Management Reporting System                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Generate data if not exists
    if not os.path.exists('data/team_performance.csv'):
        print("\n📊 Step 1: Generating management data...")
        from management_kpi_generator import ManagementKPIGenerator
        generator = ManagementKPIGenerator()
        generator.generate_all_data()
    else:
        print("\n✅ Data already exists. Skipping generation.")
    
    # Step 2: Check for alerts
    print("\n🚨 Step 2: Checking KPIs for alerts...")
    from alert_monitor import AlertMonitor
    monitor = AlertMonitor()
    alerts = monitor.check_all_kpis()
    monitor.print_alerts()
    
    # Step 3: Generate weekly report
    print("\n📄 Step 3: Generating weekly PDF report...")
    from weekly_report_generator import WeeklyReportGenerator
    report_gen = WeeklyReportGenerator()
    report_path = report_gen.generate_report()
    
    # Step 4: Send email (optional - requires configuration)
    print("\n📧 Step 4: Sending email to managers...")
    print("   Email configuration required. Run auto_email_sender.py to configure.")
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  ✅ PIPELINE COMPLETE!                                       ║
║                                                               ║
║  Generated:                                                  ║
║  - Management KPI data (CSV files in /data)                 ║
║  - Weekly PDF report (/reports/weekly_report_*.pdf)         ║
║  - Alert summary (printed above)                            ║
║                                                               ║
║  Next Steps:                                                 ║
║  1. Review alerts above                                      ║
║  2. Open Power BI and connect to /data files                ║
║  3. Configure email to send automatic reports               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

def check_status():
    """Check current pipeline status"""
    print("\n" + "="*50)
    print("MANAGEMENT DASHBOARD STATUS")
    print("="*50)
    
    files_exist = {
        'Team Data': os.path.exists('data/team_performance.csv'),
        'Project Data': os.path.exists('data/project_tracking.csv'),
        'Budget Data': os.path.exists('data/budget_vs_actual.csv'),
        'Productivity Data': os.path.exists('data/productivity_metrics.csv'),
        'Reports': len(os.listdir('reports')) if os.path.exists('reports') else 0
    }
    
    for name, exists in files_exist.items():
        status = "✅" if exists else "❌"
        print(f"{status} {name}: {exists if isinstance(exists, bool) else f'{exists} files'}")
    
    print("="*50)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Management Operations Dashboard')
    parser.add_argument('--status', action='store_true', help='Check pipeline status')
    args = parser.parse_args()
    
    if args.status:
        check_status()
    else:
        run_pipeline()