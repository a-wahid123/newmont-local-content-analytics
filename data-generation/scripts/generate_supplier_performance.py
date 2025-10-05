"""
Supplier Performance Data Generator
Generates quarterly performance assessments for suppliers
Shows performance improvement over time
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seeds
np.random.seed(42)

class PerformanceGenerator:
    def __init__(self, supplier_file='../output/supplier_registry.csv'):
        self.supplier_df = pd.read_csv(supplier_file)
        self.start_year = 2010
        self.end_year = 2025
        
    def get_base_performance(self, classification):
        """Base performance score by supplier classification"""
        base_scores = {
            'Local-Local': np.random.normal(7.5, 1.2),
            'Ghanaian Owned': np.random.normal(8.0, 1.0),
            'Ghanaian Participation': np.random.normal(8.2, 0.8),
            'Ghanaian Registered': np.random.normal(8.5, 0.7),
            'International': np.random.normal(8.8, 0.6)
        }
        return base_scores.get(classification, 7.5)
    
    def generate_performance(self):
        """Generate quarterly performance assessments"""
        
        performance_records = []
        
        for _, supplier in self.supplier_df.iterrows():
            
            # Get supplier start year
            reg_year = int(supplier['registration_date'][:4])
            supplier_start_year = max(self.start_year, reg_year)
            
            # Base performance for this supplier
            base_performance = self.get_base_performance(supplier['classification'])
            
            # Generate quarterly assessments
            for year in range(supplier_start_year, self.end_year + 1):
                for quarter in range(1, 5):
                    
                    # Skip future quarters
                    if year == 2025 and quarter > 3:
                        continue
                    
                    # Calculate experience effect (improvement over time)
                    years_experience = year - supplier_start_year + (quarter - 1) / 4.0
                    experience_boost = min(1.0, years_experience * 0.1)
                    
                    # Generate performance metrics
                    delivery_performance = max(0, min(100, 
                        base_performance * 12 + experience_boost * 5 + np.random.normal(0, 5)
                    ))
                    
                    quality_score = max(1, min(10,
                        base_performance + experience_boost + np.random.normal(0, 0.5)
                    ))
                    
                    cost_competitiveness = max(1, min(10,
                        base_performance + np.random.normal(0, 0.8)
                    ))
                    
                    safety_compliance = max(1, min(10,
                        base_performance + experience_boost * 0.5 + np.random.normal(0, 0.6)
                    ))
                    
                    contract_compliance = max(0, min(100,
                        base_performance * 11 + experience_boost * 3 + np.random.normal(0, 8)
                    ))
                    
                    innovation_score = max(1, min(10,
                        base_performance * 0.8 + np.random.normal(0, 1.2)
                    ))
                    
                    capacity_utilization = max(10, min(100,
                        60 + base_performance * 4 + np.random.normal(0, 10)
                    ))
                    
                    overall_score = (quality_score + cost_competitiveness + 
                                   safety_compliance + innovation_score) / 4.0
                    
                    # Improvement recommendations based on performance
                    if overall_score >= 9:
                        recommendation = 'None - Excellent Performance'
                    elif overall_score >= 8:
                        recommendation = 'Minor process improvements needed'
                    elif overall_score >= 7:
                        recommendation = 'Focus on delivery timelines'
                    elif overall_score >= 6:
                        recommendation = 'Enhance quality controls'
                    else:
                        recommendation = 'Comprehensive improvement plan required'
                    
                    # Contract renewal eligibility
                    if overall_score >= 8 and safety_compliance >= 8:
                        renewal_eligible = 'Yes'
                    elif overall_score >= 6:
                        renewal_eligible = 'Under Review'
                    else:
                        renewal_eligible = 'No'
                    
                    # Build performance record
                    performance = {
                        'performance_id': f'PERF{len(performance_records)+1:06d}',
                        'supplier_id': supplier['supplier_id'],
                        'year': year,
                        'quarter': quarter,
                        'assessment_date': f'{year}-{quarter*3:02d}-01',
                        'delivery_performance_pct': round(delivery_performance, 1),
                        'quality_score': round(quality_score, 1),
                        'cost_competitiveness_score': round(cost_competitiveness, 1),
                        'safety_compliance_score': round(safety_compliance, 1),
                        'contract_compliance_pct': round(contract_compliance, 1),
                        'innovation_score': round(innovation_score, 1),
                        'capacity_utilization_pct': round(capacity_utilization, 1),
                        'overall_score': round(overall_score, 1),
                        'improvement_recommendations': recommendation,
                        'contract_renewals_eligible': renewal_eligible,
                        'assessed_by': f'Assessor_{np.random.randint(1, 20):02d}'
                    }
                    
                    performance_records.append(performance)
        
        return pd.DataFrame(performance_records)

def main():
    """Main execution function"""
    
    print("Starting Supplier Performance Data Generation...")
    print("-" * 50)
    
    # Generate performance data
    generator = PerformanceGenerator()
    performance_df = generator.generate_performance()
    
    # Display summary
    print(f"\nTotal Performance Assessments: {len(performance_df)}")
    print(f"Unique Suppliers Assessed: {performance_df['supplier_id'].nunique()}")
    print(f"Years Covered: {performance_df['year'].min()} - {performance_df['year'].max()}")
    
    print("\nOverall Performance Distribution:")
    print(performance_df['overall_score'].describe())
    
    print("\nContract Renewal Eligibility:")
    print(performance_df['contract_renewals_eligible'].value_counts())
    
    print("\nImprovement Recommendations:")
    print(performance_df['improvement_recommendations'].value_counts())
    
    # Calculate average improvement over time for a sample supplier
    sample_supplier = performance_df['supplier_id'].iloc[0]
    sample_data = performance_df[performance_df['supplier_id'] == sample_supplier]
    if len(sample_data) > 1:
        first_score = sample_data.iloc[0]['overall_score']
        last_score = sample_data.iloc[-1]['overall_score']
        improvement = last_score - first_score
        print(f"\nSample Supplier Performance Trend:")
        print(f"Supplier: {sample_supplier}")
        print(f"First Assessment: {first_score}")
        print(f"Latest Assessment: {last_score}")
        print(f"Improvement: {improvement:+.1f} points")
    
    # Save to CSV
    output_path = '../output/supplier_performance.csv'
    performance_df.to_csv(output_path, index=False)
    print(f"\nData saved to: {output_path}")
    print("-" * 50)
    print("Supplier Performance Generation Complete!")

if __name__ == "__main__":
    main()