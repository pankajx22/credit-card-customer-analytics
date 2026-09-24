"""
Credit Card Customer Spending & Repayment Analytics
Author: Pankaj Sahu
Purpose: Data cleaning, exploratory analysis, KPI generation and business insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CUSTOMER_FILE = "Credit Banking_Project1.csv"
SPEND_FILE = "spend.csv"
REPAYMENT_FILE = "repayment.csv"


def load_data():
    customer = pd.read_csv(CUSTOMER_FILE)
    spend = pd.read_csv(SPEND_FILE)
    repayment = pd.read_csv(REPAYMENT_FILE)

    customer.columns = ["serial_no", "customer_id", "age", "city",
                        "credit_card_product", "credit_limit", "company", "segment"]
    spend.columns = ["serial_no", "customer_id", "month", "transaction_type", "amount"]
    repayment.columns = ["serial_no", "customer_id", "month", "amount", "unused_col"]
    return customer, spend, repayment


def clean_data(customer, spend, repayment):
    customer["age"] = pd.to_numeric(customer["age"], errors="coerce")
    valid_age = customer.loc[customer["age"].between(18, 90), "age"]
    customer.loc[~customer["age"].between(18, 90), "age"] = valid_age.mean()

    spend["amount"] = pd.to_numeric(spend["amount"], errors="coerce")
    repayment["amount"] = pd.to_numeric(repayment["amount"], errors="coerce")
    spend["month"] = pd.to_datetime(spend["month"], errors="coerce", dayfirst=True)
    repayment["month"] = pd.to_datetime(repayment["month"], errors="coerce", dayfirst=True)

    # Remove the source's unused repayment column.
    repayment = repayment.drop(columns=["unused_col"], errors="ignore")
    return customer, spend, repayment


def build_customer_analysis(customer, spend, repayment):
    spent = spend.groupby("customer_id", as_index=False)["amount"].sum()
    spent = spent.rename(columns={"amount": "total_spent"})

    repaid = repayment.groupby("customer_id", as_index=False)["amount"].sum()
    repaid = repaid.rename(columns={"amount": "total_repaid"})

    analysis = customer[[
        "customer_id", "age", "city", "credit_card_product",
        "credit_limit", "company", "segment"
    ]].merge(spent, on="customer_id", how="left").merge(repaid, on="customer_id", how="left")

    analysis[["total_spent", "total_repaid"]] = (
        analysis[["total_spent", "total_repaid"]].fillna(0)
    )
    analysis["outstanding_balance"] = (
        analysis["total_spent"] - analysis["total_repaid"]
    )
    analysis["repayment_coverage_pct"] = np.where(
        analysis["total_spent"] > 0,
        analysis["total_repaid"] / analysis["total_spent"] * 100,
        np.nan,
    )
    analysis["age_group"] = pd.cut(
        analysis["age"],
        bins=[18, 36, 54, 72, 91],
        labels=["18-35", "36-53", "54-71", "72-90"],
        right=False,
        include_lowest=True,
    )
    return analysis


def category_analysis(spend):
    category_map = {
        "JEWELLERY": "Shopping", "CLOTHES": "Shopping",
        "CAMERA": "Shopping", "COMPUTERS": "Shopping",
        "MUSIC": "Shopping", "BOOKS": "Needs",
        "FOOD": "Needs", "GROCERY": "Needs", "PETRO": "Travel",
        "AIR TICKET": "Travel", "BUS TICKET": "Travel",
        "AUTO": "Travel", "BIKE": "Travel", "CAR": "Travel",
    }
    spend["category"] = (
        spend["transaction_type"].astype(str).str.strip().str.upper()
        .map(category_map).fillna("Other")
    )
    return spend.groupby("category", as_index=False)["amount"].sum().rename(
        columns={"amount": "total_spent"}
    )


def create_summaries(analysis, spend, repayment):
    segment = analysis.groupby("segment", as_index=False).agg(
        customers=("customer_id", "nunique"),
        total_spent=("total_spent", "sum"),
        total_repaid=("total_repaid", "sum"),
        outstanding_balance=("outstanding_balance", "sum"),
    )
    segment["repayment_coverage_pct"] = (
        segment["total_repaid"] / segment["total_spent"] * 100
    )

    age = analysis.groupby("age_group", observed=False, as_index=False).agg(
        customers=("customer_id", "nunique"),
        total_spent=("total_spent", "sum"),
        total_repaid=("total_repaid", "sum"),
        outstanding_balance=("outstanding_balance", "sum"),
    )
    age["repayment_coverage_pct"] = age["total_repaid"] / age["total_spent"] * 100

    category = category_analysis(spend)
    category["share_pct"] = category["total_spent"] / category["total_spent"].sum() * 100

    monthly_spend = spend.groupby(spend["month"].dt.to_period("M"))["amount"].sum()
    monthly_repaid = repayment.groupby(repayment["month"].dt.to_period("M"))["amount"].sum()
    monthly = pd.concat(
        [monthly_spend.rename("total_spent"), monthly_repaid.rename("total_repaid")],
        axis=1
    ).fillna(0).reset_index()
    monthly = monthly.rename(columns={monthly.columns[0]: "period"})
    monthly["net_spend_minus_repayment"] = (
        monthly["total_spent"] - monthly["total_repaid"]
    )
    return segment, age, category, monthly


def plot_results(segment, age, category, monthly):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    axes[0, 0].bar(segment["segment"], segment["total_spent"])
    axes[0, 0].set_title("Total Spending by Customer Segment")
    axes[0, 0].tick_params(axis="x", rotation=35)
    axes[0, 0].set_ylabel("Spend")

    axes[0, 1].bar(age["age_group"].astype(str), age["total_spent"])
    axes[0, 1].set_title("Total Spending by Age Group")
    axes[0, 1].set_ylabel("Spend")

    axes[1, 0].bar(category["category"], category["total_spent"])
    axes[1, 0].set_title("Spending by Transaction Category")
    axes[1, 0].tick_params(axis="x", rotation=25)
    axes[1, 0].set_ylabel("Spend")

    axes[1, 1].plot(monthly["period"].astype(str), monthly["total_spent"], marker="o", label="Spent")
    axes[1, 1].plot(monthly["period"].astype(str), monthly["total_repaid"], marker="o", label="Repaid")
    axes[1, 1].set_title("Monthly Spending vs Repayment")
    axes[1, 1].tick_params(axis="x", rotation=45)
    axes[1, 1].legend()

    plt.tight_layout()
    plt.show()


def main():
    customer, spend, repayment = load_data()
    customer, spend, repayment = clean_data(customer, spend, repayment)
    analysis = build_customer_analysis(customer, spend, repayment)
    segment, age, category, monthly = create_summaries(analysis, spend, repayment)

    total_spent = analysis["total_spent"].sum()
    total_repaid = analysis["total_repaid"].sum()
    outstanding = analysis["outstanding_balance"].sum()
    coverage = total_repaid / total_spent * 100

    print("=== CREDIT CARD CUSTOMER ANALYTICS ===")
    print(f"Customers: {len(analysis):,}")
    print(f"Spending transactions: {len(spend):,}")
    print(f"Repayment transactions: {len(repayment):,}")
    print(f"Total spent: {total_spent:,.2f}")
    print(f"Total repaid: {total_repaid:,.2f}")
    print(f"Net outstanding balance: {outstanding:,.2f}")
    print(f"Repayment coverage: {coverage:.2f}%")
    print(f"Customers with positive outstanding balance: {(analysis['outstanding_balance'] > 0).sum():,}")

    print("\nTop spending segment:")
    print(segment.sort_values("total_spent", ascending=False).head(3).to_string(index=False))

    print("\nSpending categories:")
    print(category.sort_values("total_spent", ascending=False).to_string(index=False))

    print("\nAge-group summary:")
    print(age.to_string(index=False))

    print("\nMonthly summary:")
    print(monthly.to_string(index=False))

    plot_results(segment, age, category, monthly)


if __name__ == "__main__":
    main()
