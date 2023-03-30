import streamlit as st # pip install streamlit
from streamlit_option_menu import option_menu # pip install streamlit-option-menu
import pymysql.cursors # pip install pymysql
import time
import pandas as pd # pip install pandas
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode # pip install streamlit-aggrid  
import mysql.connector

# ---------------------------PAGE TITLE -----------------------------------
st.set_page_config(page_title = "SUPER MARKET SALES",
                   page_icon = ":dart:",
                   layout = "wide")

# --------------------------sidebar----------------------------------------
# Database connections
mydb = mysql.connector.connect(**st.secrets["mysql"])


selected = option_menu(
        menu_title = "MAIN MENU",
        options = ["Dashboard", "Sales Form", "Report"],
        icons = ["speedometer", "ui-checks", "table"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal"
    )
    
# -------------------------DASHBOARD --------------------------------------
if selected == "Dashboard":
    st.subheader(f"📊 {selected}")
    
    st.markdown("""
<iframe src="https://app.powerbi.com/view?r=eyJrIjoiMmQyMzA4YWYtNjAxYS00YzY1LWJhYTgtOWFiZGU3YmM3MWEzIiwidCI6IjJkMWUxN2Q0LWRlYzMtNGM4NS05MjcxLTIzYjIxZmM5ODhkMCJ9" 
width="1300" height="750">
</iframe>
""", unsafe_allow_html=True)
# -----------------------FORM ---------------------------------------------
if selected == "Sales Form":
   
    page_title = "Sales Form"
    page_icon = "📃"
    layout = "centered"
    st.title(page_title + " " + page_icon)
    
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
    
# ---------------------------- REPORT ------------------------------
if selected == "Report":
    st.subheader(f"📋 {selected}") 
     
    # cur = mydb.cursor()
    # query1 = "show tables"
    # cur.execute(query1)
    
    # tables = cur.fetchall()
    
    # for table in tables:
    
        
    #     query = "select * from sales"
    #     cur.execute(query)
    
    # pandas_dataframe = pd.read_sql(query, mydb)    
    # # st.write(pandas_dataframe)
    # AgGrid(pandas_dataframe)
    
    
    # Create a cursor object to execute SQL queries
    mycorsor = mydb.cursor()
    # Execute a SELECT query to retrieve data from a table
    mycorsor.execute("SELECT * FROM sales")
    
    data = mycorsor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycorsor.description])
    AgGrid(df) 