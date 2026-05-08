import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = os.getenv("API_URL", "https://agriops-finance-1.onrender.com")

st.set_page_config(page_title="AgriOps Finance", layout="wide")

st.title("AgriOps Finance Dashboard")

# Fetch dashboard data
response = requests.get(f"{API_URL}/analytics/kpis")

if response.status_code == 200:
    data = response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"₹{data['total_income']:,.2f}")
    col2.metric("Total Expenses", f"₹{data['total_expenses']:,.2f}")
    col3.metric("Net Profit", f"₹{data['net_profit']:,.2f}")

    col4, col5, col6, col7 = st.columns(4)

    col4.metric("Revenue / Acre", f"₹{data['revenue_per_acre']:,.2f}")
    col5.metric("Expense / Acre", f"₹{data['expense_per_acre']:,.2f}")
    col6.metric("Yield / Acre", f"{data['yield_per_acre']:,.2f} kg")
    col7.metric("Profit Margin", f"{data['net_profit_margin_percent']:,.2f}%")

else:
    st.error("Backend not connected")


st.subheader("Add Income")

crop_name = st.text_input("Crop Name")
quantity = st.number_input("Quantity Sold", min_value=0.0)
price_per_unit = st.number_input("Price Per Unit", min_value=0.0)

if st.button("Add Income"):
    requests.post(
        f"{API_URL}/income/",
        params={
            "crop_name": crop_name,
            "quantity": quantity,
            "price_per_unit": price_per_unit
        }
    )
    st.success("Income added successfully")


st.subheader("Add Expense")

category = st.text_input("Expense Category")
amount = st.number_input("Expense Amount", min_value=0.0)
description = st.text_input("Description")

if st.button("Add Expense"):
    requests.post(
        f"{API_URL}/expenses/",
        params={
            "category": category,
            "amount": amount,
            "description": description
        }
    )
    st.success("Expense added successfully")
st.subheader("Financial Visual Analytics")

income_response = requests.get(f"{API_URL}/income/")
expense_response = requests.get(f"{API_URL}/expenses/")

if income_response.status_code == 200 and expense_response.status_code == 200:
    income_data = income_response.json()
    expense_data = expense_response.json()

    income_df = pd.DataFrame(income_data)
    expense_df = pd.DataFrame(expense_data)

    if not income_df.empty:
        st.write("Income Data")
        st.dataframe(income_df)

    if not expense_df.empty:
        st.write("Expense Data")
        st.dataframe(expense_df)
st.subheader("Financial Visual Analytics")

income_df = pd.DataFrame()
expense_df = pd.DataFrame()

try:
    income_response = requests.get(f"{API_URL}/income/")
    expense_response = requests.get(f"{API_URL}/expenses/")

    if income_response.status_code == 200:
        income_df = pd.DataFrame(income_response.json())
    else:
        st.error(f"Could not load income data: {income_response.status_code}")

    if expense_response.status_code == 200:
        expense_df = pd.DataFrame(expense_response.json())
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

if not income_df.empty:
    fig_income = px.bar(
        income_df,
        x="crop_name",
        y="total_amount",
        title="Income by Crop"
    )
    st.plotly_chart(fig_income, use_container_width=True)

if not expense_df.empty:
    fig_expense = px.pie(
        expense_df,
        names="category",
        values="amount",
        title="Expense Breakdown by Category"
    )
    st.plotly_chart(fig_expense, use_container_width=True)