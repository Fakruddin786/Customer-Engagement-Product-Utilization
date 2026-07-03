import pandas as pd
import numpy as np

def calculate_kpis(df):
    """
    Calculate the exactly requested KPIs.
    Returns a dictionary of KPI names and values.
    """
    kpis = {}
    
    # 1. Engagement Retention Ratio
    # Compare churn between active and inactive members
    active_churn_rate = df[df['IsActiveMember'] == 1]['Exited'].mean()
    inactive_churn_rate = df[df['IsActiveMember'] == 0]['Exited'].mean()
    kpis['Engagement Retention Ratio'] = {
        'active_churn_rate': active_churn_rate,
        'inactive_churn_rate': inactive_churn_rate,
        'ratio': inactive_churn_rate / active_churn_rate if active_churn_rate > 0 else 0
    }
    
    # 2. Product Depth Index
    # Measure products used versus customer loyalty (retention = 1 - churn)
    avg_products = df['NumOfProducts'].mean()
    avg_retention = 1 - df['Exited'].mean()
    # Simplified index: Retention Rate * Avg Products
    kpis['Product Depth Index'] = avg_retention * avg_products
    
    # 3. High-Balance Disengagement Rate
    # Percentage of high-balance customers who are inactive or churned
    high_balance_threshold = df['Balance'].median()
    if pd.isna(high_balance_threshold): high_balance_threshold = 50000
    high_bal_df = df[df['Balance'] >= high_balance_threshold]
    
    if len(high_bal_df) > 0:
        disengaged_high_bal = high_bal_df[(high_bal_df['IsActiveMember'] == 0) | (high_bal_df['Exited'] == 1)]
        kpis['High-Balance Disengagement Rate'] = len(disengaged_high_bal) / len(high_bal_df)
    else:
        kpis['High-Balance Disengagement Rate'] = 0.0
        
    # 4. Credit Card Stickiness Score
    # Retention impact of credit card ownership
    cc_churn_rate = df[df['HasCrCard'] == 1]['Exited'].mean()
    no_cc_churn_rate = df[df['HasCrCard'] == 0]['Exited'].mean()
    cc_retention = 1 - cc_churn_rate
    no_cc_retention = 1 - no_cc_churn_rate
    # Difference in retention rate due to having a CC
    kpis['Credit Card Stickiness Score'] = cc_retention - no_cc_retention
    
    # 5. Relationship Strength Index
    # Combined engagement and product utilization score (out of 10 or 100)
    # Give points for: Active Member (+3), NumOfProducts (+2 per product up to 4), HasCrCard (+1)
    df_copy = df.copy()
    df_copy['RSI_Score'] = (df_copy['IsActiveMember'] * 3) + (df_copy['NumOfProducts'].clip(upper=4) * 2) + (df_copy['HasCrCard'] * 1)
    # Max possible score = 3 + 8 + 1 = 12
    # Normalize to 100
    df_copy['RSI_Score'] = (df_copy['RSI_Score'] / 12) * 100
    kpis['Relationship Strength Index'] = df_copy['RSI_Score'].mean()
    
    return kpis

def calculate_relationship_strength(df):
    """
    Returns the dataframe with Relationship Strength Index added for each customer.
    """
    df = df.copy()
    df['Relationship_Strength_Index'] = (df['IsActiveMember'] * 3) + (df['NumOfProducts'].clip(upper=4) * 2) + (df['HasCrCard'] * 1)
    df['Relationship_Strength_Index'] = (df['Relationship_Strength_Index'] / 12) * 100
    return df

def get_product_utilization_stats(df):
    """
    Stats for product utilization analysis.
    """
    stats = df.groupby('NumOfProducts').agg(
        Total_Customers=('CustomerId', 'count'),
        Churn_Rate=('Exited', 'mean')
    ).reset_index()
    return stats
