import streamlit as st
import calendar
from datetime import datetime 
import plotly.graph_objects as go
import mysql.connector
page_title = "Sales Form"
page_icon = "📃"
layout = "centered"

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_title + " " + page_icon)

# Database connections
mydb = mysql.connector.connect(**st.secrets["mysql"])

with st.form("Form"):
    col1 , col2 = st.columns(2)
    with col1:
        date          = st.date_input("Date :")
        branch        = st.selectbox("Branch :",["Choose the branch","A", "B", "C", "D"])
        city          = st.selectbox("City :", ["Choose the city","Salem", "Erode", "Chennai" ,"Coimbatore", "Dharmapuri", "Tripure", "Madurai"])
        customer_type = st.selectbox("Customer Type :", ["Choose the customer type","Normal", "Member"])
        member        = st.selectbox("Gender :", ["Choose the gender","Male", "Female"])
    with col2:    
        product_line  = st.selectbox("Product Line :", ["Choose the product line","Home and lifestyle", "Health and beauty", "Electronic accessories", "Food and Beverages", "Fashion accessories", "Sports and travel"])
        payments      = st.selectbox("Payment :", ["Choose the payment type","Cash", "Credit card", "Ewallet", "Gpay"])
        quantity      = st.number_input("Quantity :")
        unit_price    = st.number_input("Unit Price :")
        total         = st.number_input("Total :")
    rating            = st.number_input("Rating :", 0,5)
    # st.button("Save Data")
    if st.form_submit_button("Save Data"):
        cursor = mydb.cursor()
        query  = "INSERT INTO sales (date, branch, city, customer_type, member, product_line, payments, quantity, unit_price, total, rating) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (date, branch, city, customer_type, member, product_line, payments, quantity, unit_price, total, rating)
        cursor.execute(query, values)
        mydb.commit()
        if mydb:
            st.success("You have successfully submited")
            st.balloons()
        else:
            st.error("Check the above details")        
        
        