import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px


def format_inr(amount):
    amount = float(amount)

    integer_part, decimal_part = f"{amount:.2f}".split(".")

    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]

        parts = []

        while len(remaining) > 2:
            parts.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            parts.insert(0, remaining)

        formatted = ",".join(parts) + "," + last_three
    else:
        formatted = integer_part

    return f"₹{formatted}.{decimal_part}"

API_URL = os.getenv("API_URL", "https://agriops-finance-1.onrender.com")

st.set_page_config(page_title="AgriOps Finance", layout="wide")

st.title("Finance Dashboard")

# ---------------- KPIs ----------------
try:
    response = requests.get(f"{API_URL}/analytics/kpis")

    if response.status_code == 200:
        data = response.json()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", format_inr(data['total_income']))
        col2.metric("Total Expenses", format_inr(data['total_expenses']))
        col3.metric("Net Profit", format_inr(data['net_profit']))

        col4, col5, col6, col7 = st.columns(4)

        col4.metric(
        "Revenue / Acre",
        format_inr(data['revenue_per_acre'])
        )

        col5.metric(
            "Expense / Acre",
            format_inr(data['expense_per_acre'])
        )

        col6.metric("Yield / Acre", f"{data['yield_per_acre']:,.2f} kg")
        col7.metric("Profit Margin", f"{data['net_profit_margin_percent']:,.2f}%")
    else:
        st.error(f"Backend not connected: {response.status_code}")
        st.write(response.text)

except Exception as e:
    st.error(f"Backend not connected: {e}")


# ---------------- Add Income ----------------
st.subheader("Add Income")

crop_name = st.text_input("Crop Name")
quantity = st.number_input("Quantity Sold", min_value=0.0, key="income_quantity")
price_per_unit = st.number_input("Price Per Unit", min_value=0.0, key="income_price")

if st.button("Add Income"):
    response = requests.post(
        f"{API_URL}/income/",
        json={
            "crop_name": crop_name,
            "quantity": quantity,
            "price_per_unit": price_per_unit
        }
    )

    if response.status_code in [200, 201]:
        st.success("Income added successfully")
        st.rerun()
    else:
        st.error(f"Failed to add income: {response.status_code}")
        st.write(response.text)


# ---------------- Add Expense ----------------
st.subheader("Add Expense")

category = st.text_input("Expense Category")
amount = st.number_input("Expense Amount", min_value=0.0, key="expense_amount")
description = st.text_input("Description")

if st.button("Add Expense"):
    response = requests.post(
        f"{API_URL}/expenses/",
        json={
            "category": category,
            "amount": amount,
            "description": description
        }
    )

    if response.status_code in [200, 201]:
        st.success("Expense added successfully")
        st.rerun()
    else:
        st.error(f"Failed to add expense: {response.status_code}")
        st.write(response.text)


# ---------------- Visual Analytics ----------------
st.subheader("Financial Visual Analytics")

income_df = pd.DataFrame()
expense_df = pd.DataFrame()

try:
    income_response = requests.get(f"{API_URL}/income/")
    expense_response = requests.get(f"{API_URL}/expenses/")

    if income_response.status_code == 200:
        income_df = pd.DataFrame(income_response.json())

        income_df["created_at"] = pd.to_datetime(
            income_df["created_at"]
        ).dt.strftime("%d-%m-%Y %I:%M %p")
    
    else:
        st.error(f"Could not load income data: {income_response.status_code}")

    if expense_response.status_code == 200:
        expense_df = pd.DataFrame(expense_response.json())

        expense_df["created_at"] = pd.to_datetime(
            expense_df["created_at"]
        ).dt.strftime("%d-%m-%Y %I:%M %p")
    else:
        st.error(f"Could not load expense data: {expense_response.status_code}")

except Exception as e:
    st.error(f"Could not load income/expense data: {e}")


if not income_df.empty:
    st.write("Income Data")
    st.dataframe(income_df)

    fig_income = px.bar(
        income_df,
        x="crop_name",
        y="total_amount",
        title="Income by Crop"
    )
    st.plotly_chart(fig_income, use_container_width=True)
else:
    st.info("No income data available yet.")


if not expense_df.empty:
    st.write("Expense Data")
    st.dataframe(expense_df)

    fig_expense = px.pie(
        expense_df,
        names="category",
        values="amount",
        title="Expense Breakdown by Category"
    )
    st.plotly_chart(fig_expense, use_container_width=True)
else:
    st.info("No expense data available yet.")

# ---------------- Balance Sheet ----------------
st.subheader("Balance Sheet")

item_name = st.text_input("Item Name")
item_type = st.selectbox("Item Type", ["Asset", "Liability", "Equity"])
balance_category = st.text_input("Balance Sheet Category")
balance_amount = st.number_input("Balance Sheet Amount", min_value=0.0, key="balance_amount")
balance_description = st.text_input("Balance Sheet Description")

if st.button("Add Balance Sheet Item"):
    response = requests.post(
        f"{API_URL}/balance-sheet/",
        json={
            "item_name": item_name,
            "item_type": item_type,
            "category": balance_category,
            "amount": balance_amount,
            "description": balance_description
        }
    )

    if response.status_code in [200, 201]:
        st.success("Balance sheet item added successfully")
        st.rerun()
    else:
        st.error(f"Failed to add balance sheet item: {response.status_code}")
        st.write(response.text)


try:
    balance_summary_response = requests.get(f"{API_URL}/balance-sheet/summary")
    balance_items_response = requests.get(f"{API_URL}/balance-sheet/")

    if balance_summary_response.status_code == 200:
        summary = balance_summary_response.json()

        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Total Assets", f"₹{summary['total_assets']:,.2f}")
        b2.metric("Total Liabilities", f"₹{summary['total_liabilities']:,.2f}")
        b3.metric("Calculated Equity", f"₹{summary['calculated_equity']:,.2f}")
        b4.metric("Balance Difference", f"₹{summary['balance_difference']:,.2f}")

        if summary["is_balanced"]:
            st.success("Balance sheet is balanced")
        else:
            st.warning("Balance sheet is not balanced")

    if balance_items_response.status_code == 200:
        balance_df = pd.DataFrame(balance_items_response.json())

        if not balance_df.empty:
            balance_df["created_at"] = pd.to_datetime(
                balance_df["created_at"]
            ).dt.strftime("%d-%m-%Y %I:%M %p")

            st.write("Balance Sheet Items")
            st.dataframe(balance_df)

            fig_balance = px.pie(
                balance_df,
                names="item_type",
                values="amount",
                title="Balance Sheet Composition"
            )
            st.plotly_chart(fig_balance, use_container_width=True)
        else:
            st.info("No balance sheet items available yet.")

except Exception as e:
    st.error(f"Could not load balance sheet data: {e}")