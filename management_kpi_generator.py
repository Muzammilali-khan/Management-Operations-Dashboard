"""
Management KPI Generator - Creates sample management data
Tracks team performance, project status, budget, and productivity
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class ManagementKPIGenerator:
    """Generate realistic management KPIs for dashboard"""
    
    def __init__(self, output_dir='data'):
        self.output_dir = output_dir
        self.create_output_directory()
    
    def create_output_directory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 Created: {self.output_dir}")
    
    def generate_all_data(self):
        """Generate complete management dataset"""
        print("🔄 Generating management KPI data...")
        
        team_data = self._generate_team_performance()
        project_data = self._generate_project_tracking()
        budget_data = self._generate_budget_vs_actual()
        productivity_data = self._generate_productivity_metrics()
        
        self._save_data(team_data, project_data, budget_data, productivity_data)
        self._print_summary(team_data, project_data, budget_data)
        
        return {
            'team': team_data,
            'projects': project_data,
            'budget': budget_data,
            'productivity': productivity_data
        }
    
    def _generate_team_performance(self):
        """Generate team member performance data"""
        team_members = ['Amit Sharma', 'Priya Patel', 'Rajesh Kumar', 'Sneha Reddy', 
                        'Vikram Singh', 'Neha Gupta', 'Manish Joshi', 'Divya Nair']
        roles = ['Sales', 'Operations', 'Support', 'Sales', 'Operations', 'Support', 'Sales', 'Operations']
        
        data = []
        for i, (name, role) in enumerate(zip(team_members, roles)):
            for week in range(1, 53):  # 52 weeks
                tasks_completed = np.random.poisson(15 + (i * 2))
                revenue = round(np.random.uniform(5000, 25000), 2) if role == 'Sales' else 0
                customer_satisfaction = round(np.random.uniform(3.5, 5.0), 1)
                hours_logged = round(np.random.uniform(35, 50), 1)
                
                data.append({
                    'week': week,
                    'employee_name': name,
                    'role': role,
                    'tasks_completed': tasks_completed,
                    'revenue_generated': revenue,
                    'customer_satisfaction': customer_satisfaction,
                    'hours_logged': hours_logged,
                    'date': self._random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
                })
        
        return pd.DataFrame(data)
    
    def _generate_project_tracking(self):
        """Generate project status data"""
        projects = ['Website Redesign', 'CRM Implementation', 'Inventory System', 
                    'Customer Portal', 'Mobile App', 'Data Migration', 'Security Upgrade']
        
        statuses = ['On Track', 'At Risk', 'Delayed', 'Completed']
        
        data = []
        for project in projects:
            for month in range(1, 13):
                completion = min(100, np.random.randint(0, 100) + (month * 8))
                status = random.choices(statuses, weights=[0.6, 0.2, 0.1, 0.1])[0]
                budget_used = round(np.random.uniform(10000, 50000), 2)
                days_delayed = max(0, np.random.normal(5, 10)) if status == 'Delayed' else 0
                
                data.append({
                    'month': month,
                    'project_name': project,
                    'completion_percentage': min(100, completion),
                    'status': status,
                    'budget_used': budget_used,
                    'days_delayed': int(days_delayed)
                })
        
        return pd.DataFrame(data)
    
    def _generate_budget_vs_actual(self):
        """Generate budget tracking data"""
        categories = ['Marketing', 'Salaries', 'Operations', 'IT', 'Rent', 'Utilities', 'Training']
        months = list(range(1, 13))
        
        data = []
        for category in categories:
            for month in months:
                budget = round(np.random.uniform(10000, 50000), 2)
                variance = round(np.random.uniform(-0.15, 0.15), 2)
                actual = round(budget * (1 + variance), 2)
                
                data.append({
                    'month': month,
                    'category': category,
                    'budget': budget,
                    'actual': actual,
                    'variance_percent': round(variance * 100, 1),
                    'status': 'Over Budget' if actual > budget else 'Under Budget'
                })
        
        return pd.DataFrame(data)
    
    def _generate_productivity_metrics(self):
        """Generate daily productivity data"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31')
        
        data = []
        for date in dates:
            tasks = np.random.poisson(120)  # 120 tasks per day on average
            completion_rate = round(np.random.uniform(0.7, 0.98), 2)
            avg_response_time = round(np.random.uniform(2, 12), 1)
            
            data.append({
                'date': date,
                'daily_tasks': tasks,
                'completion_rate': completion_rate,
                'avg_response_time_hours': avg_response_time
            })
        
        return pd.DataFrame(data)
    
    def _random_date(self, start, end):
        return start + timedelta(days=random.randint(0, (end - start).days))
    
    def _save_data(self, team, projects, budget, productivity):
        team.to_csv(f'{self.output_dir}/team_performance.csv', index=False)
        projects.to_csv(f'{self.output_dir}/project_tracking.csv', index=False)
        budget.to_csv(f'{self.output_dir}/budget_vs_actual.csv', index=False)
        productivity.to_csv(f'{self.output_dir}/productivity_metrics.csv', index=False)
        print(f"💾 Data saved to {self.output_dir}/")
    
    def _print_summary(self, team, projects, budget):
        print("\n" + "="*50)
        print("MANAGEMENT DATA GENERATED SUCCESSFULLY")
        print("="*50)
        print(f"👥 Team Members: {team['employee_name'].nunique()}")
        print(f"📊 Projects Tracked: {projects['project_name'].nunique()}")
        print(f"💰 Total Budget: ₹{budget['budget'].sum():,.2f}")
        print(f"⚠️ At Risk Projects: {len(projects[projects['status'] == 'At Risk'])}")
        print("="*50)

if __name__ == "__main__":
    generator = ManagementKPIGenerator()
    generator.generate_all_data()