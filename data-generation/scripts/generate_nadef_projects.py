"""
NADeF Community Projects Data Generator
Generates Newmont Ahafo Development Foundation project data
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seeds
np.random.seed(42)
random.seed(42)

class NADeFGenerator:
    def __init__(self, num_projects=200):
        self.num_projects = num_projects
        
        # Communities near Ahafo mine
        self.communities = [
            'Kenyasi No. 1', 'Kenyasi No. 2', 'Ntotoroso', 'Yamfo', 'Terchire',
            'Wamahinso', 'Susuanso', 'Afrisipa', 'Gyedu', 'Hwidiem'
        ]
        
        # Project categories
        self.categories = [
            'Education', 'Healthcare', 'Infrastructure', 'Economic Development',
            'Agriculture', 'Water & Sanitation', 'Skills Training', 
            'Youth Development', 'Women Empowerment', 'Environmental Conservation'
        ]
        
        self.statuses = ['Planning', 'Active', 'Completed', 'On Hold', 'Cancelled']
        
    def get_project_name(self, category, community):
        """Generate project name based on category"""
        names = {
            'Education': f'{community} School Construction/Renovation',
            'Healthcare': f'{community} Health Clinic Development',
            'Infrastructure': f'{community} Road/Bridge Construction',
            'Economic Development': f'{community} Market Development',
            'Agriculture': f'{community} Agricultural Training Program',
            'Water & Sanitation': f'{community} Water System Installation',
            'Skills Training': f'{community} Vocational Training Center',
            'Youth Development': f'{community} Youth Center Development',
            'Women Empowerment': f'{community} Women\'s Cooperative Program',
            'Environmental Conservation': f'{community} Environmental Protection Initiative'
        }
        return names.get(category, f'{community} Community Project')
    
    def get_budget_range(self, category):
        """Budget ranges by project type"""
        ranges = {
            'Education': (25000, 150000),
            'Healthcare': (50000, 200000),
            'Infrastructure': (75000, 400000),
            'Economic Development': (20000, 100000),
            'Agriculture': (15000, 75000),
            'Water & Sanitation': (40000, 180000),
            'Skills Training': (30000, 120000),
            'Youth Development': (20000, 80000),
            'Women Empowerment': (10000, 50000),
            'Environmental Conservation': (15000, 60000)
        }
        return ranges.get(category, (10000, 100000))
    
    def get_project_duration(self, category):
        """Duration in months by project type"""
        durations = {
            'Education': [6, 9, 12, 18],
            'Healthcare': [4, 6, 9, 12],
            'Infrastructure': [8, 12, 18, 24],
            'Economic Development': [3, 6, 9, 12],
            'Agriculture': [6, 9, 12],
            'Water & Sanitation': [4, 6, 8, 12],
            'Skills Training': [3, 6, 9, 12],
            'Youth Development': [6, 12, 18],
            'Women Empowerment': [6, 9, 12],
            'Environmental Conservation': [12, 18, 24, 36]
        }
        return random.choice(durations.get(category, [6, 12]))
    
    def calculate_beneficiaries(self, category, budget):
        """Estimate beneficiaries based on category and budget"""
        multipliers = {
            'Education': 50,
            'Healthcare': 200,
            'Infrastructure': 500,
            'Economic Development': 100,
            'Agriculture': 75,
            'Water & Sanitation': 300,
            'Skills Training': 25,
            'Youth Development': 150,
            'Women Empowerment': 50,
            'Environmental Conservation': 1000
        }
        
        multiplier = multipliers.get(category, 100)
        beneficiaries = int(budget / 1000 * multiplier / 100)
        return max(10, beneficiaries)
    
    def generate_projects(self):
        """Generate NADeF community projects"""
        
        projects = []
        start_date = datetime(2006, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        for i in range(self.num_projects):
            
            # Basic project info
            category = random.choice(self.categories)
            community = random.choice(self.communities)
            project_name = self.get_project_name(category, community)
            
            # Budget
            min_budget, max_budget = self.get_budget_range(category)
            budget = np.random.uniform(min_budget, max_budget)
            
            # Project dates
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            project_start = start_date + timedelta(days=random_days)
            
            duration_months = self.get_project_duration(category)
            project_end = project_start + timedelta(days=duration_months * 30)
            
            # Status based on timeline
            if project_end < datetime.now():
                status = np.random.choice(['Completed', 'Cancelled'], p=[0.92, 0.08])
            elif project_start <= datetime.now() <= project_end:
                status = 'Active'
            else:
                status = np.random.choice(['Planning', 'On Hold'], p=[0.85, 0.15])
            
            # Actual spend based on status
            if status == 'Completed':
                actual_spend = budget * np.random.uniform(0.85, 1.15)
            elif status == 'Active':
                progress = (datetime.now() - project_start).days / (project_end - project_start).days
                progress = max(0, min(1, progress))
                actual_spend = budget * progress * np.random.uniform(0.8, 1.1)
            elif status == 'Cancelled':
                actual_spend = budget * np.random.uniform(0.1, 0.4)
            else:  # Planning or On Hold
                actual_spend = budget * np.random.uniform(0, 0.1)
            
            # Completion percentage
            if status == 'Completed':
                completion_pct = 100
            elif status == 'Cancelled':
                completion_pct = np.random.uniform(10, 40)
            elif status == 'Active':
                completion_pct = progress * 100
            else:
                completion_pct = 0
            
            # Beneficiaries
            beneficiaries = self.calculate_beneficiaries(category, budget)
            
            # Impact score (only for completed projects)
            if status == 'Completed':
                budget_efficiency = actual_spend / budget if budget > 0 else 1
                if 0.9 <= budget_efficiency <= 1.1:
                    impact_score = np.random.uniform(7, 10)
                else:
                    impact_score = np.random.uniform(5, 8)
            elif status == 'Active':
                impact_score = np.random.uniform(6, 9)
            elif status == 'Cancelled':
                impact_score = np.random.uniform(1, 4)
            else:
                impact_score = None
            
            # Build project record
            project = {
                'project_id': f'NAD{i+1:04d}',
                'project_name': project_name,
                'community': community,
                'category': category,
                'start_date': project_start.strftime('%Y-%m-%d'),
                'end_date': project_end.strftime('%Y-%m-%d'),
                'budget_usd': round(budget, 2),
                'actual_spend_usd': round(actual_spend, 2),
                'beneficiaries_count': beneficiaries,
                'status': status,
                'impact_score': round(impact_score, 1) if impact_score else None,
                'completion_percentage': round(completion_pct, 1),
                'project_manager': f'PM_{random.randint(1, 25):02d}',
                'implementing_partner': random.choice([
                    'NADeF Direct', 'Local NGO', 'Government Partnership', 
                    'International NGO', 'Community-led'
                ]),
                'funding_source': random.choice([
                    'NADeF Core', 'Special Projects Fund', 'Partnership Fund'
                ])
            }
            
            projects.append(project)
        
        return pd.DataFrame(projects)

def main():
    """Main execution function"""
    
    print("Starting NADeF Community Projects Data Generation...")
    print("-" * 50)
    
    # Generate projects
    generator = NADeFGenerator(num_projects=200)
    projects_df = generator.generate_projects()
    
    # Display summary
    print(f"\nTotal Projects Generated: {len(projects_df)}")
    print(f"Communities Served: {projects_df['community'].nunique()}")
    print(f"Total Budget: ${projects_df['budget_usd'].sum():,.2f}")
    print(f"Total Actual Spend: ${projects_df['actual_spend_usd'].sum():,.2f}")
    print(f"Total Beneficiaries: {projects_df['beneficiaries_count'].sum():,}")
    
    print("\nProjects by Status:")
    print(projects_df['status'].value_counts())
    
    print("\nProjects by Category:")
    print(projects_df['category'].value_counts())
    
    print("\nProjects by Community:")
    print(projects_df['community'].value_counts())
    
    # Calculate completion rate
    completed = len(projects_df[projects_df['status'] == 'Completed'])
    total_closed = completed + len(projects_df[projects_df['status'] == 'Cancelled'])
    if total_closed > 0:
        completion_rate = (completed / total_closed) * 100
        print(f"\nProject Success Rate: {completion_rate:.1f}%")
    
    # Average impact score for completed projects
    completed_projects = projects_df[projects_df['status'] == 'Completed']
    if len(completed_projects) > 0:
        avg_impact = completed_projects['impact_score'].mean()
        print(f"Average Impact Score (Completed): {avg_impact:.1f}/10")
    
    # Save to CSV
    output_path = '../output/nadef_projects.csv'
    projects_df.to_csv(output_path, index=False)
    print(f"\nData saved to: {output_path}")
    print("-" * 50)
    print("NADeF Community Projects Generation Complete!")

if __name__ == "__main__":
    main()