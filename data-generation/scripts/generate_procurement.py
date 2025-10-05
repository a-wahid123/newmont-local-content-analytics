"""
Procurement Transactions Data Generator
Generates realistic procurement transaction data with local content tracking
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seeds
np.random.seed(42)
random.seed(42)

class ProcurementGenerator:
    def __init__(self, supplier_file='../output/supplier_registry.csv', num_transactions=5000):
        self.num_transactions = num_transactions
        self.supplier_df = pd.read_csv(supplier_file)
        
        # Procurement categories
        self.departments = [
            'Mining Operations', 'Maintenance', 'Administration', 
            'Security', 'Environmental', 'Community Relations'
        ]
        
        self.tender_types = ['Open Tender', 'Restricted Tender', 'Direct Award']
        self.payment_terms = ['Net 30', 'Net 60', 'Net 90', 'Upon Delivery']
        self.delivery_locations = ['Ahafo South', 'Ahafo North', 'Subika', 'Accra Office']
        self.contract_statuses = ['Active', 'Completed', 'Cancelled']
        
    def get_contract_value_range(self, classification, category):
        """Determine realistic contract value based on supplier type and category"""
        
        base_ranges = {
            'Local-Local': (5000, 50000),
            'Ghanaian Owned': (10000, 200000),
            'Ghanaian Participation': (25000, 500000),
            'Ghanaian Registered': (50000, 1000000),
            'International': (100000, 5000000)
        }
        
        min_val, max_val = base_ranges[classification]
        
        # Adjust for category
        high_value_categories = ['Construction Services', 'Equipment Rental', 'Equipment Parts']
        if category in high_value_categories:
            min_val *= 2
            max_val *= 3
            
        return min_val, max_val
    
    def calculate_local_content(self, classification):
        """Calculate local content percentage based on supplier classification"""
        
        local_content_ranges = {
            'Local-Local': (95, 100),
            'Ghanaian Owned': (70, 95),
            'Ghanaian Participation': (30, 70),
            'Ghanaian Registered': (10, 40),
            'International': (0, 15)
        }
        
        min_pct, max_pct = local_content_ranges[classification]
        return np.random.uniform(min_pct, max_pct)
    
    def inject_data_quality_issues(self, df):
        """Add realistic data quality problems"""
        
        # Missing PO numbers (3%)
        missing_po_idx = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
        df.loc[missing_po_idx, 'po_number'] = None
        
        # Currency mixing - some in GHS instead of USD (5%)
        ghs_idx = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
        df.loc[ghs_idx, 'currency'] = 'GHS'
        # Convert USD to GHS (approximate rate)
        for idx in ghs_idx:
            df.loc[idx, 'contract_value_usd'] *= 12.5
        
        # Missing delivery locations (2%)
        missing_loc_idx = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
        df.loc[missing_loc_idx, 'delivery_location'] = None
        
        # Outlier contract values (1%)
        outlier_idx = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
        for idx in outlier_idx:
            current_value = df.loc[idx, 'contract_value_usd']
            df.loc[idx, 'contract_value_usd'] = current_value * np.random.uniform(5, 10)
        
        return df
    
    def generate_transactions(self):
        """Generate procurement transactions with realistic patterns"""
        
        transactions = []
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2025, 9, 30)
        
        for i in range(self.num_transactions):
            
            # Transaction date
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            transaction_date = start_date + timedelta(days=random_days)
            year = transaction_date.year
            
            # Local content policy effect - increase local preference over time
            local_bias = min(0.7, 0.2 + (year - 2010) * 0.03)
            
            # Select supplier with local preference
            if np.random.random() < local_bias:
                local_suppliers = self.supplier_df[
                    self.supplier_df['classification'].isin(['Local-Local', 'Ghanaian Owned'])
                ]
                if len(local_suppliers) > 0:
                    supplier = local_suppliers.sample(1).iloc[0]
                else:
                    supplier = self.supplier_df.sample(1).iloc[0]
            else:
                supplier = self.supplier_df.sample(1).iloc[0]
            
            # Contract value
            min_val, max_val = self.get_contract_value_range(
                supplier['classification'], 
                supplier['primary_category']
            )
            contract_value = np.random.uniform(min_val, max_val)
            
            # Contract duration
            if 'Services' in supplier['primary_category']:
                duration_months = random.choice([1, 3, 6, 12, 24, 36])
            else:
                duration_months = random.choice([1, 2, 3])
            
            # Department allocation
            dept_weights = [0.4, 0.2, 0.1, 0.1, 0.1, 0.1]
            department = np.random.choice(self.departments, p=dept_weights)
            
            # Tender type based on contract value
            if contract_value > 100000:
                tender_type = np.random.choice(['Open Tender', 'Restricted Tender'], p=[0.8, 0.2])
            elif contract_value > 25000:
                tender_type = np.random.choice(
                    ['Open Tender', 'Restricted Tender', 'Direct Award'], 
                    p=[0.5, 0.3, 0.2]
                )
            else:
                tender_type = np.random.choice(['Restricted Tender', 'Direct Award'], p=[0.3, 0.7])
            
            # Local content percentage
            local_content_pct = self.calculate_local_content(supplier['classification'])
            
            # Contract dates
            contract_start = transaction_date
            contract_end = contract_start + timedelta(days=duration_months * 30)
            
            # Contract status
            if contract_end < datetime.now():
                status = np.random.choice(['Completed', 'Cancelled'], p=[0.95, 0.05])
            elif contract_start <= datetime.now() <= contract_end:
                status = 'Active'
            else:
                status = 'Active'
            
            # Build transaction record
            transaction = {
                'transaction_id': f'TXN{i+1:06d}',
                'supplier_id': supplier['supplier_id'],
                'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                'contract_value_usd': round(contract_value, 2),
                'currency': 'USD',
                'category': supplier['primary_category'],
                'subcategory': supplier['secondary_category'],
                'department': department,
                'contract_duration_months': duration_months,
                'tender_type': tender_type,
                'local_content_percentage': round(local_content_pct, 1),
                'payment_terms': random.choice(self.payment_terms),
                'contract_start_date': contract_start.strftime('%Y-%m-%d'),
                'contract_end_date': contract_end.strftime('%Y-%m-%d'),
                'po_number': f'PO{random.randint(100000, 999999)}',
                'delivery_location': random.choice(self.delivery_locations),
                'project_code': f'PRJ{random.randint(1000, 9999)}',
                'budget_code': f'BUD{random.randint(100, 999)}',
                'approval_level': random.choice(['Manager', 'Director', 'VP', 'SVP']),
                'contract_status': status
            }
            
            transactions.append(transaction)
        
        # Create DataFrame
        df = pd.DataFrame(transactions)
        
        # Inject data quality issues
        df = self.inject_data_quality_issues(df)
        
        return df

def main():
    """Main execution function"""
    
    print("Starting Procurement Transactions Data Generation...")
    print("-" * 50)
    
    # Generate transactions
    generator = ProcurementGenerator(num_transactions=5000)
    transactions_df = generator.generate_transactions()
    
    # Calculate statistics
    total_value = transactions_df['contract_value_usd'].sum()
    local_suppliers = transactions_df.merge(
        generator.supplier_df[['supplier_id', 'classification']], 
        on='supplier_id'
    )
    
    local_local_value = local_suppliers[
        local_suppliers['classification'].isin(['Local-Local', 'Ghanaian Owned'])
    ]['contract_value_usd'].sum()
    
    local_content_pct = (local_local_value / total_value) * 100
    
    # Display summary
    print(f"\nTotal Transactions Generated: {len(transactions_df)}")
    print(f"Total Contract Value: ${total_value:,.2f}")
    print(f"Local Content Spend: ${local_local_value:,.2f}")
    print(f"Local Content Percentage: {local_content_pct:.1f}%")
    
    print("\nTransactions by Tender Type:")
    print(transactions_df['tender_type'].value_counts())
    
    print("\nTransactions by Status:")
    print(transactions_df['contract_status'].value_counts())
    
    print("\nData Quality Issues (Intentional):")
    print(f"Missing PO Numbers: {transactions_df['po_number'].isna().sum()}")
    print(f"Currency Mixing (GHS): {(transactions_df['currency'] == 'GHS').sum()}")
    print(f"Missing Delivery Locations: {transactions_df['delivery_location'].isna().sum()}")
    
    # Save to CSV
    output_path = '../output/procurement_transactions.csv'
    transactions_df.to_csv(output_path, index=False)
    print(f"\nData saved to: {output_path}")
    print("-" * 50)
    print("Procurement Transactions Generation Complete!")

if __name__ == "__main__":
    main()