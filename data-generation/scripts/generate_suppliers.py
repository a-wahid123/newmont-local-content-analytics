"""
Supplier Registry Data Generator
Generates realistic supplier data with Ghana's 5-tier classification system
Includes intentional data quality issues for cleaning practice
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Initialize Faker
try:
    from faker import Faker
    fake = Faker()
    Faker.seed(42)
except ImportError:
    print("Warning: Faker not installed. Using simplified name generation.")
    fake = None

class SupplierGenerator:
    def __init__(self, num_suppliers=500):
        self.num_suppliers = num_suppliers
        
        # Ghanaian company name components
        self.ghana_prefixes = [
            'Ahafo', 'Asante', 'Kumasi', 'Accra', 'Tema', 'Brong', 
            'Ghana', 'Golden', 'West Africa', 'Ashanti', 'Volta'
        ]
        
        self.business_types = [
            'Services', 'Enterprise', 'Trading', 'Construction', 
            'Engineering', 'Logistics', 'Solutions', 'Industries',
            'Mining Services', 'Technical', 'Supplies'
        ]
        
        self.legal_suffixes = ['Ltd', 'Limited', 'Co Ltd', '']
        
        # Service categories
        self.service_categories = [
            'Construction Services', 'Transportation & Logistics', 'Catering Services',
            'Security Services', 'Equipment Rental', 'Maintenance Services',
            'IT Services', 'Consulting Services', 'Environmental Services',
            'Medical Services', 'Training Services', 'Waste Management',
            'Electrical Services', 'Mechanical Services', 'Civil Works',
            'Supplies & Materials', 'Equipment Parts', 'Safety Equipment',
            'Office Supplies', 'Fuel & Lubricants', 'Laboratory Services',
            'Legal Services', 'Accounting Services', 'Financial Services'
        ]
        
    def generate_company_name(self, classification):
        """Generate company name based on classification"""
        
        if classification in ['Local-Local', 'Ghanaian Owned']:
            prefix = random.choice(self.ghana_prefixes)
            business_type = random.choice(self.business_types)
            suffix = random.choice(self.legal_suffixes)
            
            if suffix:
                name = f"{prefix} {business_type} {suffix}"
            else:
                name = f"{prefix} {business_type}"
                
        elif classification == 'Ghanaian Participation':
            if fake:
                intl_name = fake.company().split()[0]
            else:
                intl_name = f"Company{random.randint(1,999)}"
            ghana_suffix = random.choice(['Ghana', 'West Africa'])
            suffix = random.choice(['Ltd', 'Limited'])
            name = f"{intl_name} {ghana_suffix} {suffix}"
            
        elif classification == 'Ghanaian Registered':
            if fake:
                name = f"{fake.company()} Ghana {random.choice(['Ltd', 'Limited'])}"
            else:
                name = f"International{random.randint(1,999)} Ghana Ltd"
                
        else:  # International
            if fake:
                name = fake.company()
            else:
                name = f"Global Corp {random.randint(1,999)}"
            
        return name
    
    def generate_contact_info(self):
        """Generate contact information"""
        if fake:
            return {
                'name': fake.name(),
                'phone': fake.phone_number(),
                'email': fake.email(),
                'address': fake.address().replace('\n', ', ')
            }
        else:
            num = random.randint(1000, 9999)
            return {
                'name': f"Contact Person {num}",
                'phone': f"+233-{random.randint(200000000, 599999999)}",
                'email': f"contact{num}@company.com",
                'address': f"{random.randint(1,999)} Main Street, Accra"
            }
    
    def inject_data_quality_issues(self, df):
        """Add realistic data quality problems"""
        
        # Missing phone numbers (10%)
        missing_phone_idx = np.random.choice(df.index, size=int(len(df) * 0.1), replace=False)
        df.loc[missing_phone_idx, 'phone'] = None
        
        # Missing emails (8%)
        missing_email_idx = np.random.choice(df.index, size=int(len(df) * 0.08), replace=False)
        df.loc[missing_email_idx, 'email'] = None
        
        # Company name variations (5%)
        variation_idx = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
        for idx in variation_idx:
            name = df.loc[idx, 'company_name']
            if 'Ltd' in name and 'Limited' not in name:
                df.loc[idx, 'company_name'] = name.replace('Ltd', 'Limited')
            elif 'Limited' in name:
                df.loc[idx, 'company_name'] = name.replace('Limited', 'Ltd')
        
        # Ownership percentage precision issues (15%)
        precision_idx = np.random.choice(df.index, size=int(len(df) * 0.15), replace=False)
        for idx in precision_idx:
            current_value = df.loc[idx, 'ownership_percentage']
            df.loc[idx, 'ownership_percentage'] = round(current_value + np.random.uniform(-0.5, 0.5), 4)
        
        # Missing certification status (5%)
        missing_cert_idx = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
        df.loc[missing_cert_idx, 'certification_status'] = None
        
        return df
    
    def generate_suppliers(self):
        """Generate complete supplier registry dataset"""
        
        suppliers = []
        
        # Classification distribution
        classifications = np.random.choice(
            ['Local-Local', 'Ghanaian Owned', 'Ghanaian Participation', 
             'Ghanaian Registered', 'International'],
            size=self.num_suppliers,
            p=[0.15, 0.25, 0.20, 0.25, 0.15]
        )
        
        for i, classification in enumerate(classifications):
            
            # Company name
            company_name = self.generate_company_name(classification)
            
            # Ownership and distance based on classification
            if classification == 'Local-Local':
                ownership_pct = np.random.uniform(80, 100)
                distance_km = np.random.uniform(1, 25)
            elif classification == 'Ghanaian Owned':
                ownership_pct = np.random.uniform(51, 95)
                distance_km = np.random.uniform(25, 200)
            elif classification == 'Ghanaian Participation':
                ownership_pct = np.random.uniform(10, 50)
                distance_km = np.random.uniform(50, 300)
            elif classification == 'Ghanaian Registered':
                ownership_pct = np.random.uniform(0, 20)
                distance_km = np.random.uniform(100, 400)
            else:  # International
                ownership_pct = 0
                distance_km = np.random.uniform(500, 5000)
            
            # Registration date
            if classification in ['Local-Local', 'Ghanaian Owned']:
                start_year = 2010
            else:
                start_year = 2006
            
            year = np.random.randint(start_year, 2025)
            month = np.random.randint(1, 13)
            day = np.random.randint(1, 29)
            reg_date = datetime(year, month, day)
            
            # Annual revenue
            years_operating = (datetime.now() - reg_date).days / 365.0
            
            base_revenue_map = {
                'Local-Local': np.random.uniform(50000, 500000),
                'Ghanaian Owned': np.random.uniform(200000, 2000000),
                'Ghanaian Participation': np.random.uniform(500000, 5000000),
                'Ghanaian Registered': np.random.uniform(1000000, 10000000),
                'International': np.random.uniform(5000000, 50000000)
            }
            
            base_revenue = base_revenue_map[classification]
            annual_revenue = base_revenue * (1 + years_operating * 0.1)
            
            # Employee count
            employees = max(1, int(annual_revenue / 100000 * np.random.uniform(0.5, 2.0)))
            
            # Contact information
            contact = self.generate_contact_info()
            
            # Build supplier record
            supplier = {
                'supplier_id': f'SUP{i+1:04d}',
                'company_name': company_name,
                'classification': classification,
                'ownership_percentage': round(ownership_pct, 1),
                'distance_from_mine_km': round(distance_km, 1),
                'registration_date': reg_date.strftime('%Y-%m-%d'),
                'primary_category': random.choice(self.service_categories),
                'secondary_category': random.choice(self.service_categories),
                'annual_revenue_usd': round(annual_revenue, 2),
                'certification_status': random.choice(['Certified', 'Pending', 'Not Certified']),
                'contact_person': contact['name'],
                'phone': contact['phone'],
                'email': contact['email'],
                'address': contact['address'],
                'tax_id': f'TIN{random.randint(10000000, 99999999)}',
                'employees_count': employees,
                'founded_year': year,
                'website': f"www.{company_name.lower().replace(' ', '').replace('ltd', '').replace('limited', '').replace(',', '')}.com.gh" if classification != 'International' else f"www.company{i}.com"
            }
            
            suppliers.append(supplier)
        
        # Create DataFrame
        df = pd.DataFrame(suppliers)
        
        # Inject data quality issues
        df = self.inject_data_quality_issues(df)
        
        return df

def main():
    """Main execution function"""
    
    print("Starting Supplier Registry Data Generation...")
    print("-" * 50)
    
    # Generate suppliers
    generator = SupplierGenerator(num_suppliers=500)
    supplier_df = generator.generate_suppliers()
    
    # Display summary
    print(f"\nTotal Suppliers Generated: {len(supplier_df)}")
    print("\nSupplier Classification Distribution:")
    print(supplier_df['classification'].value_counts())
    
    print("\nCertification Status Distribution:")
    print(supplier_df['certification_status'].value_counts())
    
    print("\nData Quality Issues (Intentional):")
    print(f"Missing Phone Numbers: {supplier_df['phone'].isna().sum()}")
    print(f"Missing Emails: {supplier_df['email'].isna().sum()}")
    print(f"Missing Certification Status: {supplier_df['certification_status'].isna().sum()}")
    
    # Save to CSV
    output_path = '../output/supplier_registry.csv'
    supplier_df.to_csv(output_path, index=False)
    print(f"\nData saved to: {output_path}")
    print("-" * 50)
    print("Supplier Registry Generation Complete!")

if __name__ == "__main__":
    main()