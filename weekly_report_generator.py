"""
Weekly Report Generator - Creates PDF report for management
"""

import pandas as pd
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

class WeeklyReportGenerator:
    """Generate weekly PDF report for management"""
    
    def __init__(self, data_dir='data', output_dir='reports'):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.create_output_directory()
    
    def create_output_directory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 Created: {self.output_dir}")
    
    def generate_report(self):
        """Generate complete weekly report"""
        print("\n📄 Generating weekly management report...")
        
        # Load data
        team_df = pd.read_csv(f'{self.data_dir}/team_performance.csv')
        project_df = pd.read_csv(f'{self.data_dir}/project_tracking.csv')
        budget_df = pd.read_csv(f'{self.data_dir}/budget_vs_actual.csv')
        productivity_df = pd.read_csv(f'{self.data_dir}/productivity_metrics.csv')
        
        # Calculate weekly summaries
        latest_week = int(team_df['week'].max())  # Convert to int
        week_data = team_df[team_df['week'] == latest_week]
        latest_month = int(budget_df['month'].max())  # Convert to int
        
        report_data = {
            'week_number': latest_week,
            'week_range': self._get_week_range(latest_week),
            'total_tasks': int(week_data['tasks_completed'].sum()),
            'avg_satisfaction': float(week_data['customer_satisfaction'].mean()),
            'total_revenue': float(week_data['revenue_generated'].sum()),
            'active_projects': int(len(project_df[project_df['status'].isin(['On Track', 'At Risk'])])),
            'at_risk_projects': int(len(project_df[project_df['status'] == 'At Risk'])),
            'budget_variance': float(budget_df[budget_df['month'] == latest_month]['variance_percent'].mean()),
            'productivity_rate': float(productivity_df['completion_rate'].iloc[-7:].mean())
        }
        
        self._create_pdf(report_data, week_data, project_df, budget_df)
        
        return f"{self.output_dir}/weekly_report_week_{latest_week}.pdf"
    
    def _get_week_range(self, week_num):
        """Calculate date range for the week"""
        week_num = int(week_num)
        start_date = datetime(2024, 1, 1) + timedelta(weeks=week_num-1)
        end_date = start_date + timedelta(days=6)
        return f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"
    
    def _create_pdf(self, report_data, week_data, project_df, budget_df):
        """Create PDF document"""
        filename = f"{self.output_dir}/weekly_report_week_{report_data['week_number']}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30)
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=12, spaceAfter=10)
        
        story = []
        
        # Title
        story.append(Paragraph(f"Management Weekly Report - Week {report_data['week_number']}", title_style))
        story.append(Paragraph(f"Period: {report_data['week_range']}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        
        status_icon = "✓" if report_data['avg_satisfaction'] >= 4.0 else "⚠️"
        budget_status = "✓" if abs(report_data['budget_variance']) <= 10 else "⚠️"
        risk_status = "⚠️" if report_data['at_risk_projects'] > 0 else "✓"
        
        summary_data = [
            ["Metric", "Value", "Status"],
            [f"Total Tasks Completed", f"{report_data['total_tasks']:,}", "✓"],
            [f"Avg Customer Satisfaction", f"{report_data['avg_satisfaction']:.1f}/5.0", status_icon],
            [f"Total Revenue", f"₹{report_data['total_revenue']:,.2f}", "✓"],
            [f"Active Projects", report_data['active_projects'], "✓"],
            [f"At Risk Projects", report_data['at_risk_projects'], risk_status],
            [f"Avg Budget Variance", f"{report_data['budget_variance']:.1f}%", budget_status],
            [f"Productivity Rate", f"{report_data['productivity_rate']:.1%}", "✓"]
        ]
        
        table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Team Performance
        story.append(Paragraph("Team Performance - Top Performers", heading_style))
        top_performers = week_data.nlargest(3, 'tasks_completed')[['employee_name', 'tasks_completed', 'customer_satisfaction']]
        top_table = [["Employee", "Tasks Completed", "Satisfaction"]]
        for _, row in top_performers.iterrows():
            top_table.append([row['employee_name'], str(int(row['tasks_completed'])), f"{row['customer_satisfaction']:.1f}"])
        
        team_table = Table(top_table, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        team_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(team_table)
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("Management Recommendations", heading_style))
        recommendations = []
        
        if report_data['at_risk_projects'] > 0:
            recommendations.append("• Escalate at-risk projects to leadership for additional resources")
        if abs(report_data['budget_variance']) > 10:
            recommendations.append("• Review budget categories with >10% variance for cost optimization")
        if report_data['productivity_rate'] < 0.75:
            recommendations.append("• Investigate productivity drop and remove process bottlenecks")
        if not recommendations:
            recommendations.append("• Continue current strategy - all KPIs are within targets")
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        print(f"✅ Report saved: {filename}")
        
        return filename

if __name__ == "__main__":
    generator = WeeklyReportGenerator()
    generator.generate_report()