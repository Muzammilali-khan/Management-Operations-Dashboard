# Management Operations Dashboard

Management reporting system with automated alerts, PDF reports, and Power BI dashboard.

## Features

- Tracks team performance, project status, budget, and productivity
- Automated alerts when KPIs fall below thresholds
- Weekly PDF report generation
- Interactive 3-page Power BI dashboard

## Dashboard Previews

### Executive Dashboard
![Executive Dashboard](dashboard-executive.png)

### Project Tracking
![Project Dashboard](dashboard-project.png)

### Budget Analysis
![Budget Dashboard](dashboard-budget.png)

## Sample Report
[Download Sample PDF Report](sample-report.pdf)

## Tech Stack

- Python (data generation, ETL, alerts, PDF)
- Power BI (dashboard)
- ReportLab (PDF generation)
- Pandas (data processing)


## Files

| File | Purpose |
|------|---------|
| `management_kpi_generator.py` | Generate sample management data |
| `alert_monitor.py` | Check KPIs and trigger alerts |
| `weekly_report_generator.py` | Create PDF report |
| `auto_email_sender.py` | Email reports to managers |
| `main.py` | Run complete pipeline |
| `management_dashboard.pbix` | Power BI dashboard |

## Setup

```bash
pip install -r requirements.txt
python management_kpi_generator.py
python main.py
