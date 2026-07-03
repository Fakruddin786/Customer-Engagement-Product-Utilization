import pandas as pd
import numpy as np
import os

def load_data(file_path):
    """
    Load dataset, display shape and basic info.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at {file_path}")
    
    df = pd.read_csv(file_path)
    print("Dataset Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    return df

def validate_and_clean_data(df):
    """
    Validates binary variables, engagement fields, and handles missing values.
    """
    # Required columns based on the problem statement
    expected_cols = [
        "CustomerId", "Surname", "CreditScore", "Geography", "Gender", 
        "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", 
        "IsActiveMember", "EstimatedSalary", "Exited"
    ]
    
    # Check for missing expected columns
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")
        
    df = df[expected_cols].copy()
    
    # Check for missing values and duplicates
    missing_count = df.isnull().sum().sum()
    duplicate_count = df.duplicated().sum()
    
    if duplicate_count > 0:
        df = df.drop_duplicates()
        
    # Drop rows with critical missing values if any
    df = df.dropna()
    
    # Ensure binary fields are correct
    for col in ['HasCrCard', 'IsActiveMember', 'Exited']:
        df[col] = df[col].astype(int)
        
    return df

def create_engagement_profiles(df):
    """
    Create customer engagement profiles based on activity, balance, and products.
    Profiles:
    - Active Engaged Customers
    - Inactive Disengaged Customers
    - Active but Low Product Customers
    - Inactive High Balance Customers
    """
    df = df.copy()
    
    # Define thresholds
    high_balance_threshold = df['Balance'].median() if df['Balance'].median() > 0 else df[df['Balance']>0]['Balance'].median()
    if pd.isna(high_balance_threshold): high_balance_threshold = 50000
    
    def assign_profile(row):
        is_active = row['IsActiveMember'] == 1
        has_high_balance = row['Balance'] >= high_balance_threshold
        multi_product = row['NumOfProducts'] > 1
        
        if is_active and multi_product:
            return "Active Engaged Customers"
        elif not is_active and not multi_product and not has_high_balance:
            return "Inactive Disengaged Customers"
        elif is_active and not multi_product:
            return "Active but Low Product Customers"
        elif not is_active and has_high_balance:
            return "Inactive High Balance Customers"
        else:
            return "Other Customers"
            
    df['EngagementProfile'] = df.apply(assign_profile, axis=1)
    return df
