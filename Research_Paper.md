# Research Paper: Customer Engagement & Product Utilization Analytics for Retention Strategy

## 1. Abstract
This paper investigates the determinants of customer churn in the banking sector by shifting the focus from traditional demographic analysis to behavioral engagement and product utilization. Utilizing a dataset of 10,000 customers, we calculate custom Key Performance Indicators (KPIs) to quantify relationship depth and present a programmatic approach to identifying at-risk premium customers.

## 2. Introduction & Problem Statement
Banks often struggle with retention models that over-index on financial health (e.g., high balance or salary). Consequently, they face "silent churn," where financially healthy customers quietly disengage and eventually leave. This study aims to evaluate the precise relationship between behavioral engagement, product mix, and churn probability.

## 3. Methodology
### 3.1 Data Ingestion & Validation
The analysis was performed on a focused 13-column dataset including variables such as `IsActiveMember`, `NumOfProducts`, `Balance`, and `Exited`. Binary fields were validated, and missing values were handled to maintain data integrity.

### 3.2 Engagement Classification
Customers were segmented into four distinct profiles based on behavioral thresholds:
- Active Engaged Customers (Active + Multi-product)
- Inactive Disengaged Customers (Inactive + Low Balance/Single Product)
- Active but Low Product Customers (Active + Single Product)
- Inactive High Balance Customers (Inactive + Above Median Balance)

### 3.3 Key Performance Indicators
Five distinct metrics were formulated to assess loyalty:
1. **Engagement Retention Ratio**: Comparing the churn rates of active versus inactive users.
2. **Product Depth Index**: A measure combining product count with historical retention loyalty.
3. **High-Balance Disengagement Rate**: The percentage of high-balance customers showing inactivity.
4. **Credit Card Stickiness Score**: The delta in retention impact driven by credit card ownership.
5. **Relationship Strength Index**: A unified weighted score (0-100) combining activity, product count, and credit card ownership.

## 4. Exploratory Data Analysis (EDA) & Insights
### 4.1 Product Utilization Impact
Analysis of `NumOfProducts` vs. `Exited` reveals a nonlinear relationship. Customers with 1 product exhibit high churn (lack of integration). Customers with 2 products show the lowest churn (optimal stickiness). Interestingly, customers with 3 or 4 products show a sharp increase in churn, often indicative of over-leverage or poor service scaling.

### 4.2 Financial Commitment vs. Engagement
The cross-analysis of `Balance` vs. `IsActiveMember` highlighted the "At-Risk Premium" segment. These are customers with balances exceeding the median who have ceased regular banking activity. This segment represents the highest potential loss of Assets Under Management (AUM).

### 4.3 Retention Strength
The calculated Relationship Strength Index (RSI) acts as a strong inverse predictor of churn. As RSI transitions from Low to Medium, the churn probability drops exponentially, validating the hypothesis that deep behavioral ties supersede demographic traits.

## 5. Recommendations & Future Scope
- **Product Bundling**: Introduce "Day 1" bundles that ensure new customers immediately adopt 2 products (e.g., checking + savings or checking + credit card).
- **Proactive Interventions**: Implement automated triggers when a high-balance customer's activity drops for 60 consecutive days.
- **Future Enhancements**: Transition these analytical findings into a predictive Machine Learning pipeline (e.g., Random Forest or Gradient Boosting) to forecast real-time churn probability at the individual customer level.

## 6. Conclusion
Retention strategies must pivot from demographic assumptions to behavioral realities. By measuring engagement depth and product utilization, banks can optimize their retention spend and drastically reduce the silent churn of valuable customers.
