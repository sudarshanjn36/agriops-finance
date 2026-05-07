import streamlit as st
import requests

API_URL = "http://backend:8000"

st.set_page_config(page_title="AgriOps Finance", layout="wide")

st.title("AgriOps Finance Dashboard")

# Fetch dashboard data
response = requests.get(f"{API_URL}/dashboard/")

if response.status_code == 200:
    data = response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"₹{data['total_income']:,.2f}")
    col2.metric("Total Expenses", f"₹{data['total_expenses']:,.2f}")
    col3.metric("Net Profit", f"₹{data['net_profit']:,.2f}")
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