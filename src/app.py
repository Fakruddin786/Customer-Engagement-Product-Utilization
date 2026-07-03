import streamlit as st
import pandas as pd
import os

from preprocessing import load_data, validate_and_clean_data, create_engagement_profiles
from analysis import calculate_kpis, calculate_relationship_strength
from dashboard import render_kpis, render_module_1, render_module_2, render_module_3, render_module_4

# Set page config
st.set_page_config(
    page_title="Customer Engagement & Retention",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Removed Custom CSS to allow native light/dark themes to work automatically

@st.cache_data
def load_and_prep_data():
    """Loads and preprocesses data."""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'customer_churn.csv')
    try:
        df = load_data(data_path)
        df = validate_and_clean_data(df)
        df = create_engagement_profiles(df)
        df = calculate_relationship_strength(df)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def main():
    st.title("Customer Engagement & Product Utilization Analytics")
    st.markdown("### Strategy for Customer Retention")
    
    df = load_and_prep_data()
    
    if df.empty:
        st.warning("Please ensure 'customer_churn.csv' is placed in the 'data/' folder.")
        return
        
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("User Filters")
    
    # Engagement Status
    engagement_options = ['All'] + list(df['EngagementProfile'].unique())
    selected_engagement = st.sidebar.selectbox("Engagement Status", engagement_options)
    
    # Number of Products
    prod_min, prod_max = int(df['NumOfProducts'].min()), int(df['NumOfProducts'].max())
    selected_products = st.sidebar.slider("Number of Products", prod_min, prod_max, (prod_min, prod_max))
    
    # Balance Threshold
    bal_min, bal_max = float(df['Balance'].min()), float(df['Balance'].max())
    selected_balance = st.sidebar.slider("Balance Range", bal_min, bal_max, (bal_min, bal_max))
    
    # Salary Threshold
    sal_min, sal_max = float(df['EstimatedSalary'].min()), float(df['EstimatedSalary'].max())
    selected_salary = st.sidebar.slider("Estimated Salary Range", sal_min, sal_max, (sal_min, sal_max))
    
    # --- APPLY FILTERS ---
    filtered_df = df.copy()
    if selected_engagement != 'All':
        filtered_df = filtered_df[filtered_df['EngagementProfile'] == selected_engagement]
        
    filtered_df = filtered_df[
        (filtered_df['NumOfProducts'] >= selected_products[0]) &
        (filtered_df['NumOfProducts'] <= selected_products[1])
    ]
    
    filtered_df = filtered_df[
        (filtered_df['Balance'] >= selected_balance[0]) &
        (filtered_df['Balance'] <= selected_balance[1])
    ]
    
    filtered_df = filtered_df[
        (filtered_df['EstimatedSalary'] >= selected_salary[0]) &
        (filtered_df['EstimatedSalary'] <= selected_salary[1])
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"Showing {len(filtered_df)} out of {len(df)} customers based on filters.")
    
    if len(filtered_df) == 0:
        st.warning("No customers match the selected filters.")
        return
        
    # --- RENDER DASHBOARD ---
    
    # KPIs
    kpis = calculate_kpis(filtered_df)
    render_kpis(kpis)
    st.markdown("---")
    
    # Tabs for Modules
    tab1, tab2, tab3, tab4 = st.tabs([
        "Engagement vs Churn", 
        "Product Utilization", 
        "Disengaged Premium Detector", 
        "Retention Strength Score"
    ])
    
    with tab1:
        render_module_1(filtered_df)
        
    with tab2:
        render_module_2(filtered_df)
        
    with tab3:
        render_module_3(filtered_df)
        
    with tab4:
        render_module_4(filtered_df)

if __name__ == "__main__":
    main()
