import streamlit as st
import pandas as pd
from utils import (
    create_bar_chart, create_pie_chart, create_scatter_plot, 
    create_histogram, create_box_plot, create_heatmap, format_insight
)
from analysis import get_product_utilization_stats

def render_kpis(kpis):
    """
    Render KPI metrics in Streamlit.
    """
    st.markdown("### Key Performance Indicators")
    cols = st.columns(5)
    
    with cols[0]:
        val = kpis.get('Engagement Retention Ratio', {}).get('ratio', 0)
        st.metric("Engagement Retention Ratio", f"{val:.2f}x")
    
    with cols[1]:
        val = kpis.get('Product Depth Index', 0)
        st.metric("Product Depth Index", f"{val:.2f}")
        
    with cols[2]:
        val = kpis.get('High-Balance Disengagement Rate', 0) * 100
        st.metric("High-Bal Disengagement Rate", f"{val:.1f}%")
        
    with cols[3]:
        val = kpis.get('Credit Card Stickiness Score', 0) * 100
        st.metric("CC Stickiness Score", f"{val:+.1f}%")
        
    with cols[4]:
        val = kpis.get('Relationship Strength Index', 0)
        st.metric("Relationship Strength (Avg)", f"{val:.1f}/100")

def render_module_1(df):
    """
    Module 1: Engagement vs Churn Overview
    """
    st.header("Module 1: Engagement vs Churn Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Active vs Inactive Customers Distribution
        active_counts = df['IsActiveMember'].value_counts().reset_index()
        active_counts['IsActiveMember'] = active_counts['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
        fig1 = create_pie_chart(active_counts, 'IsActiveMember', 'count', "Active vs Inactive Customer Base")
        st.plotly_chart(fig1, use_container_width=True)
        
        st.info(format_insight(
            what="Proportion of active vs inactive members in the bank.",
            why="Activity is usually driven by regular transactions, digital logins, or product usage.",
            impact="A high proportion of inactive members suggests a large segment at risk of silent churn.",
            strategy="Implement re-engagement campaigns like targeted transaction cashback or app-login bonuses."
        ))

    with col2:
        # Churn by Activity Status
        churn_by_activity = df.groupby('IsActiveMember')['Exited'].mean().reset_index()
        churn_by_activity['IsActiveMember'] = churn_by_activity['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
        churn_by_activity['Churn Rate (%)'] = churn_by_activity['Exited'] * 100
        fig2 = create_bar_chart(churn_by_activity, 'IsActiveMember', 'Churn Rate (%)', "Churn Rate by Activity Status", text=churn_by_activity['Churn Rate (%)'].round(1).astype(str)+'%')
        st.plotly_chart(fig2, use_container_width=True)
        
        st.info(format_insight(
            what="Compares the churn rate between active and inactive customers.",
            why="Inactive customers have lower switching costs and less dependency on the bank's ecosystem.",
            impact="Shows exactly how much disengagement drives attrition, leading to revenue loss.",
            strategy="Require periodic interaction (e.g., update KYC via app) to keep accounts 'active' or offer rewards for maintaining activity."
        ))

def render_module_2(df):
    """
    Module 2: Product Utilization Impact Analysis
    """
    st.header("Module 2: Product Utilization Impact Analysis")
    
    stats = get_product_utilization_stats(df)
    stats['Churn Rate (%)'] = stats['Churn_Rate'] * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Product Count Distribution
        fig1 = create_bar_chart(stats, 'NumOfProducts', 'Total_Customers', "Customer Distribution by Product Count")
        fig1.update_xaxes(type='category')
        st.plotly_chart(fig1, use_container_width=True)
        
        st.info(format_insight(
            what="Number of customers holding 1, 2, 3, or 4 products.",
            why="Most customers typically start with a single checking/savings account.",
            impact="A heavy skew towards 1 product means low cross-sell success and weaker relationships.",
            strategy="Design introductory bundles (e.g., account + credit card) for new joiners."
        ))

    with col2:
        # Product Count vs Churn
        fig2 = create_bar_chart(stats, 'NumOfProducts', 'Churn Rate (%)', "Churn Rate by Product Count", color='Churn Rate (%)')
        fig2.update_xaxes(type='category')
        st.plotly_chart(fig2, use_container_width=True)
        
        st.info(format_insight(
            what="Churn percentage broken down by the number of products held.",
            why="Customers with 2 products are usually the most sticky. Oddly, 3-4 products sometimes show high churn if they represent bad debt/credit issues.",
            impact="Highlights the optimal 'sweet spot' for product bundling.",
            strategy="Focus on transitioning 1-product customers to 2-product customers, rather than forcing 3+ products."
        ))

    st.markdown("---")
    st.subheader("Distribution of Tenure by Product Count")
    fig3 = create_box_plot(df, 'NumOfProducts', 'Tenure', 'Exited', "Tenure Distribution by Product Count")
    fig3.update_xaxes(type='category')
    st.plotly_chart(fig3, use_container_width=True)
    
    st.info(format_insight(
        what="Box plot displaying customer tenure distribution across different product counts, split by churn status.",
        why="Helps identify if customers with certain product counts leave earlier or stay longer.",
        impact="Provides deeper clarity into the lifecycle of multi-product vs single-product customers.",
        strategy="If multi-product customers leave early, review the onboarding experience for bundled products."
    ))

def render_module_3(df):
    """
    Module 3: High-Value Disengaged Customer Detector
    """
    st.header("Module 3: High-Value Disengaged Customer Detector")
    st.markdown("Use this panel to identify customers who have high balances or salaries but are disengaged.")
    
    high_val_disengaged = df[
        (df['EngagementProfile'].isin(['Inactive High Balance Customers', 'Inactive Disengaged Customers'])) &
        (df['Balance'] > df['Balance'].median())
    ]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Total At-Risk Premium Customers", len(high_val_disengaged))
        churned_prem = len(high_val_disengaged[high_val_disengaged['Exited']==1])
        st.metric("Churned within this group", churned_prem)
        
    with col2:
        fig = create_scatter_plot(high_val_disengaged, 'Age', 'Balance', color='Exited', title="Premium Disengaged Customers (Age vs Balance)")
        st.plotly_chart(fig, use_container_width=True)
        
    st.info(format_insight(
        what="Scatter plot of disengaged customers with above-median balances.",
        why="These customers parked money but stopped transacting, often finding better yields elsewhere.",
        impact="Loss of these customers severely impacts the bank's asset base (AUM).",
        strategy="Assign Relationship Managers to call these clients. Offer premium wealth management products or higher yield deposits."
    ))
        
    with st.expander("View Filtered Customer Data"):
        st.dataframe(high_val_disengaged[['CustomerId', 'Surname', 'Age', 'Balance', 'EstimatedSalary', 'NumOfProducts', 'Exited']].head(100))

def render_module_4(df):
    """
    Module 4: Retention Strength Scoring Panel
    """
    st.header("Module 4: Retention Strength Scoring Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Engagement Profile Distribution
        profile_counts = df['EngagementProfile'].value_counts().reset_index()
        fig1 = create_pie_chart(profile_counts, 'EngagementProfile', 'count', "Engagement Profile Distribution")
        st.plotly_chart(fig1, use_container_width=True)
        
        st.info(format_insight(
            what="Distribution of customers across behavior-based engagement profiles.",
            why="Classifies customers beyond demographics into actionable behavioral cohorts.",
            impact="Helps marketing teams size their target audiences for different retention campaigns.",
            strategy="Allocate budget proportionally to shift 'Inactive Disengaged' to 'Active Low Product'."
        ))
        
    with col2:
        # Relationship Strength Index vs Churn
        # Bin RSI into categories
        df['RSI_Tier'] = pd.cut(df['Relationship_Strength_Index'], bins=[0, 33, 66, 100], labels=['Low', 'Medium', 'High'])
        rsi_churn = df.groupby('RSI_Tier', observed=False)['Exited'].mean().reset_index()
        rsi_churn['Churn Rate (%)'] = rsi_churn['Exited'] * 100
        
        fig2 = create_bar_chart(rsi_churn, 'RSI_Tier', 'Churn Rate (%)', "Churn Rate by Relationship Strength Tier")
        st.plotly_chart(fig2, use_container_width=True)
        
        st.info(format_insight(
            what="Churn rate segmented by Relationship Strength Index (Low, Medium, High).",
            why="The RSI aggregates multiple stickiness factors (activity, products, credit cards).",
            impact="Validates that deeper relationships (higher RSI) statistically reduce churn.",
            strategy="Use RSI as a primary KPI for frontline staff bonuses. Focus on moving customers from Low to Medium RSI."
        ))
        
    st.markdown("---")
    st.subheader("Feature Correlation Heatmap")
    
    # Select numeric columns for heatmap
    numeric_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary', 'Relationship_Strength_Index', 'Exited']
    corr_matrix = df[numeric_cols].corr()
    
    fig3 = create_heatmap(corr_matrix, "Correlation Matrix of Customer Attributes")
    st.plotly_chart(fig3, use_container_width=True)
    
    st.info(format_insight(
        what="Heatmap showing the correlation coefficients between numerical variables and churn.",
        why="Identifies which variables move together and which are most strongly associated with churn (Exited).",
        impact="Reveals non-obvious relationships, like how Age and Balance might correlate with Churn.",
        strategy="Use highly correlated features to build predictive models or targeted risk flags."
    ))
