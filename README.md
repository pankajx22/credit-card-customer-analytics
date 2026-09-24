# README

# Credit Card Customer Spending & Repayment Analytics

## Overview

This project analyzes customer credit-card spending and repayment behavior using Python. The objective is to convert transaction-level data into KPIs, trends, customer-segment patterns, spending-category patterns, and repayment indicators that can support business decisions.

## Problem Statement

Financial institutions need to understand how customers spend and repay credit. This analysis examines spending, repayment, age groups, customer segments, transaction categories, and outstanding balances to identify measurable patterns and areas for further review.

## Dataset

The project uses three CSV files:

- `Credit Banking_Project1.csv` — customer profile, age, city, credit-card product, limit, company and segment.
- `spend.csv` — customer spending transactions.
- `repayment.csv` — customer repayment transactions.
- [Customer dataset — Credit Banking_Project1.csv](https://github.com/pankajx22/credit-card-customer-analytics/blob/main/Credit%20Banking_Project1.csv)
- [Spending dataset — spend.csv](https://github.com/pankajx22/credit-card-customer-analytics/blob/main/spend.csv)
- [Repayment dataset — repayment.csv](https://github.com/pankajx22/credit-card-customer-analytics/blob/main/repayment.csv)

The files are included with this project submission.

## Methodology

1. Load the three datasets.
2. Standardize column names and source-field inconsistencies.
3. Validate customer age values and replace invalid ages with the mean of valid ages.
4. Convert transaction amounts to numeric values and dates to datetime.
5. Aggregate spending and repayment at customer level.
6. Calculate outstanding balance and repayment coverage.
7. Analyze customer segments, age groups, transaction categories and monthly trends.
8. Visualize the results and translate them into business observations.

## Key Results

- Customers analyzed: **100**
- Spending transactions: **1,500**
- Repayment transactions: **1,523**
- Total spending: **381,352,045.00**
- Total repayment: **371,208,444.12**
- Net outstanding balance (spending minus repayment): **10,143,600.88**
- Repayment coverage: **97.34%**
- Customers with positive outstanding balance: **55**

## Important observations

- The customer segment with the highest aggregate spending is **Normal Salary**.
- The highest-spend age group is **36-53**.
- The largest mapped spending category is **Travel**.
- Outstanding balance is calculated as aggregate spending minus aggregate repayment; it is an analytical indicator and should not be interpreted as an accounting statement of an individual bill without additional billing-cycle information.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib

## How to Run

1. Install Python 3.10+.
2. Install dependencies:
`pip install -r requirements.txt`
3. Keep the three CSV files in the same folder as `PankajSahu_CreditBankingAnalysis.py`.
4. Run:
`python PankajSahu_CreditBankingAnalysis.py`

## Project Structure

```
Pankaj_Credit_Banking_Analysis/
├── PankajSahu_CreditBankingAnalysis.py
├── requirements.txt
├── README.md
├── Credit Banking_Project1.csv
├── spend.csv
└── repayment.csv
```

## Scope and Limitation

The dataset is transaction-based and does not provide a full statement-level accounting view. Therefore, outstanding balance and repayment coverage are analytical indicators derived from the available spending and repayment records. Correlation or group differences should not be interpreted as causation.