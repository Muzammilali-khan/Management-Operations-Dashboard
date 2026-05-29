"""
Alert Monitor - Checks KPIs and sends alerts when metrics fall below thresholds
"""

import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class AlertMonitor:
    """Monitor KPIs and trigger alerts for management"""
    
    def __init__(self, data_dir='data', alert_thresholds=None):
        self.data_dir = data_dir
        self.alert_thresholds = alert_thresholds or {
            'completion_rate': 0.75,      # Below 75% completion rate
            'customer_satisfaction': 4.0,  # Below 4.0 satisfaction
            'budget_variance': 10,         # Over 10% budget variance
            'days_delayed': 7,              # Delayed more than 7 days
            'tasks_completed': 50          # Less than 50 tasks per week
        }
        self.alerts = []
    
    def check_all_kpis(self):
        """Check all KPIs and collect alerts"""
        print("\n🔍 Checking management KPIs...")
        
        # Check productivity metrics
        self._check_productivity()
        
        # Check team performance
        self._check_team_performance()
        
        # Check project status
        self._check_projects()
        
        # Check budget
        self._check_budget()
        
        return self.alerts
    
    def _check_productivity(self):
        """Check productivity metrics"""
        try:
            df = pd.read_csv(f'{self.data_dir}/productivity_metrics.csv')
            latest = df.iloc[-7:]  # Last 7 days
            avg_completion = latest['completion_rate'].mean()
            
            if avg_completion < self.alert_thresholds['completion_rate']:
                self.alerts.append({
                    'severity': 'HIGH',
                    'category': 'Productivity',
                    'message': f"Completion rate dropped to {avg_completion:.1%}. Target: {self.alert_thresholds['completion_rate']:.0%}",
                    'action': 'Review team workload and remove blockers'
                })
        except Exception as e:
            print(f"Error checking productivity: {e}")
    
    def _check_team_performance(self):
        """Check team performance metrics"""
        try:
            df = pd.read_csv(f'{self.data_dir}/team_performance.csv')
            latest_week = df[df['week'] == df['week'].max()]
            low_performers = latest_week[latest_week['tasks_completed'] < self.alert_thresholds['tasks_completed']]
            
            if not low_performers.empty:
                for _, emp in low_performers.iterrows():
                    self.alerts.append({
                        'severity': 'MEDIUM',
                        'category': 'Team Performance',
                        'message': f"{emp['employee_name']} completed only {emp['tasks_completed']} tasks this week",
                        'action': 'Schedule 1:1 meeting to identify challenges'
                    })
            
            low_satisfaction = latest_week[latest_week['customer_satisfaction'] < self.alert_thresholds['customer_satisfaction']]
            if not low_satisfaction.empty:
                for _, emp in low_satisfaction.iterrows():
                    self.alerts.append({
                        'severity': 'HIGH',
                        'category': 'Customer Satisfaction',
                        'message': f"{emp['employee_name']} has satisfaction score {emp['customer_satisfaction']}",
                        'action': 'Review recent customer feedback and provide coaching'
                    })
        except Exception as e:
            print(f"Error checking team performance: {e}")
    
    def _check_projects(self):
        """Check project status"""
        try:
            df = pd.read_csv(f'{self.data_dir}/project_tracking.csv')
            at_risk = df[df['status'] == 'At Risk']
            delayed = df[df['days_delayed'] > self.alert_thresholds['days_delayed']]
            
            for _, project in at_risk.iterrows():
                self.alerts.append({
                    'severity': 'HIGH',
                    'category': 'Projects',
                    'message': f"Project '{project['project_name']}' is at risk. Completion: {project['completion_percentage']}%",
                    'action': 'Escalate to steering committee for additional resources'
                })
            
            for _, project in delayed.iterrows():
                self.alerts.append({
                    'severity': 'MEDIUM',
                    'category': 'Projects',
                    'message': f"Project '{project['project_name']}' delayed by {project['days_delayed']} days",
                    'action': 'Review project plan and adjust timeline'
                })
        except Exception as e:
            print(f"Error checking projects: {e}")
    
    def _check_budget(self):
        """Check budget variances"""
        try:
            df = pd.read_csv(f'{self.data_dir}/budget_vs_actual.csv')
            over_budget = df[abs(df['variance_percent']) > self.alert_thresholds['budget_variance']]
            
            for _, item in over_budget.iterrows():
                self.alerts.append({
                    'severity': 'HIGH' if item['variance_percent'] > 20 else 'MEDIUM',
                    'category': 'Budget',
                    'message': f"{item['category']} is {item['variance_percent']:.1f}% over budget for month {item['month']}",
                    'action': 'Review expenses and identify cost-saving opportunities'
                })
        except Exception as e:
            print(f"Error checking budget: {e}")
    
    def print_alerts(self):
        """Print alerts to console"""
        if not self.alerts:
            print("\n✅ No alerts. All KPIs are within acceptable ranges.")
            return
        
        print("\n" + "="*60)
        print(f"🚨 ALERTS - {len(self.alerts)} issues require attention")
        print("="*60)
        
        high_alerts = [a for a in self.alerts if a['severity'] == 'HIGH']
        medium_alerts = [a for a in self.alerts if a['severity'] == 'MEDIUM']
        
        if high_alerts:
            print("\n🔴 HIGH SEVERITY - Immediate attention required:")
            for alert in high_alerts:
                print(f"   • [{alert['category']}] {alert['message']}")
                print(f"     → Action: {alert['action']}")
        
        if medium_alerts:
            print("\n🟡 MEDIUM SEVERITY - Review this week:")
            for alert in medium_alerts:
                print(f"   • [{alert['category']}] {alert['message']}")
                print(f"     → Action: {alert['action']}")
    
    def get_alert_summary(self):
        """Return alert summary as dictionary for email"""
        return {
            'total_alerts': len(self.alerts),
            'high_count': len([a for a in self.alerts if a['severity'] == 'HIGH']),
            'medium_count': len([a for a in self.alerts if a['severity'] == 'MEDIUM']),
            'alerts': self.alerts,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == "__main__":
    monitor = AlertMonitor()
    alerts = monitor.check_all_kpis()
    monitor.print_alerts()