# Customer Engagement & Product Utilization Analytics for Retention Strategy

## Project Overview
Banks increasingly recognize that customer behavior and engagement—not just demographics—determine long-term retention. Customers may appear financially strong but still churn due to low engagement, limited product adoption, or weak relationship depth. This project evaluates retention through the lens of customer behavior and relationship strength.

## Problem Statement
Despite having data on customer engagement and product usage, banks often lack:
- Quantitative insight into which behaviors drive retention.
- Clarity on whether product depth reduces churn.
- Evidence on whether high balances alone ensure customer loyalty.

As a result, retention strategies are frequently generic and misaligned with actual customer behavior. This analytics solution evaluates customer engagement, product utilization, and customer relationship strength to support data-driven retention strategies.

## Objectives
- Evaluate the relationship between engagement and churn.
- Measure retention impact of product count and product mix.
- Identify disengaged yet high-value customers.
- Support engagement-driven retention strategies and product bundling decisions.
- Reduce silent churn among premium customers.

## Dataset Description
The dataset focuses on customer churn modeling and includes:
- **CustomerId**, **Surname**: Identifiers.
- **CreditScore**, **Geography**, **Gender**, **Age**: Demographics and credit history.
- **Tenure**, **Balance**, **EstimatedSalary**: Financial metrics.
- **NumOfProducts**, **HasCrCard**, **IsActiveMember**: Engagement and utilization metrics.
- **Exited**: Target variable (Churn).

## Project Structure
```text
Customer_Engagement_Product_Utilization/
├── data/
├── notebooks/
├── models/
├── src/
│   ├── app.py
│   ├── dashboard.py
│   ├── preprocessing.py
│   ├── analysis.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Installation & How to Run
1. Clone this repository and navigate to the root directory.
2. Ensure you have Python installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place the dataset `customer_churn.csv` inside the `data/` folder.
5. Run the Streamlit application:
   ```bash
   streamlit run src/app.py
   ```

## Requirements
See `requirements.txt` for the list of required packages:
- streamlit
- pandas
- numpy
- plotly
- matplotlib
- scikit-learn
- openpyxl

## Dashboard Features
- **Engagement vs Churn Overview**: Explores active vs. inactive customer churn behavior.
- **Product Utilization Impact Analysis**: Evaluates how the number of products held affects loyalty.
- **High-Value Disengaged Customer Detector**: An interactive filtering panel to discover "At-Risk Premium Customers."
- **Retention Strength Scoring Panel**: Assesses overall relationship strength index based on various engagement behaviors.

## Key Performance Indicators (KPIs)
1. **Engagement Retention Ratio**: Compares churn between active and inactive members.
2. **Product Depth Index**: Measures products used vs customer loyalty.
3. **High-Balance Disengagement Rate**: Percentage of high-balance customers who are inactive or churned.
4. **Credit Card Stickiness Score**: Retention impact of credit card ownership.
5. **Relationship Strength Index**: Combined engagement and product utilization score.

## Business Insights
The application dynamically provides business insights below visualizations. These help explain patterns (e.g., higher churn among single-product users), business impacts, and suggested retention strategies (e.g., cross-selling secondary products).

## Future Scope
- Integration with live databases and data warehouses.
- Implementation of predictive machine learning models to forecast real-time churn probability.
- Automated email/notification triggers for at-risk high-value customers.
