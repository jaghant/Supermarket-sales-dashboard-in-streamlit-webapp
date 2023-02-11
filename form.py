import streamlit as st # pip install streamlit
from streamlit_option_menu import option_menu # pip install streamlit-option-menu
import pymysql.cursors # pip install pymysql
import time
import pandas as pd # pip install pandas
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode # pip install streamlit-aggrid  

# ---------------------------PAGE TITLE -----------------------------------
st.set_page_config(page_title = "SUPER MARKET SALES",
                   page_icon = ":dart:",
                   layout = "wide")

# --------------------------sidebar----------------------------------------

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Dashboard", "Form", "Report"],
        icons = ["speedometer", "ui-checks", "table"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "parallel"
    )
    
# -------------------------DASHBOARD --------------------------------------
if selected == "Dashboard":
    st.subheader(f"📊 {selected}")
    
    st.markdown("""
<iframe src="https://app.powerbi.com/view?r=eyJrIjoiMmQyMzA4YWYtNjAxYS00YzY1LWJhYTgtOWFiZGU3YmM3MWEzIiwidCI6IjJkMWUxN2Q0LWRlYzMtNGM4NS05MjcxLTIzYjIxZmM5ODhkMCJ9" 
width="1400" height="800">
</iframe>
""", unsafe_allow_html=True)
# -----------------------FORM ---------------------------------------------
if selected == "Form":
    # connect to database
    
    
    # Create the sales form
    left_column, middle_column, right_column = st.columns(3)
    with middle_column:
        st.subheader("📃Sales Form")
    connection = pymysql.connect(host = "localhost",
                                 port = 3306,
                                 user = "root",
                                 password = "Dell@123",
                                 db = "powerapps",
                                 charset = "utf8mb4",
                                 cursorclass = pymysql.cursors.DictCursor)    
    left_column, right_column = st.columns(2)
    
    with left_column:    
        date          = st.date_input("Date :")
        branch        = st.selectbox("Branch :", ["A","B","C","D"])
        city          = st.selectbox("City :", ["Salem", "Erode"])
        customer_type = st.selectbox("Customer Type :", ["Normal", "Member"])
        gender        = st.selectbox("Gender :", ["Male", "Female"])
    with right_column:    
        product_line  = st.selectbox("Product Line :", ["Home and lifestyle", "Health and beauty", "Electronic accessories", "Food and beverages", "Fashion accessories", "Sports and travel"])
        Payment       = st.selectbox("Payment :", ["Cash","Credit card", "Ewallet", "Gpay"])
        Quantity      = st.number_input("Quantity :")
        unit_price    = st.number_input("Unit Price :")
        total         = st.number_input("Total :")
    rating        = st.number_input("Rating :", 0,5)
    
# Insert the values into the sales_details database
    if st.button("Submit"):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO supermarket_sales(date, branch, city, customer_type, gender, product_line, unit_price, quantity, total, payment, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (date, branch, city, customer_type, gender, product_line, unit_price, Quantity, total, Payment, rating))
            connection.commit()
            st.success("The form is Successfully submited ✔")     
        except Exception as e:
            st.error("Error: {}".format(e))
    connection.close()        
# ---------------------------- REPORT ------------------------------
if selected == "Report":
    st.subheader(f"📋 {selected}") 
    
    connection = pymysql.connect(host = "localhost",
                                 port = 3306,
                                 user = "root",
                                 password = "Dell@123",
                                 db = "powerapps",
                                 charset = "utf8mb4",
                                 cursorclass = pymysql.cursors.DictCursor)
     
    cur = connection.cursor()
    query1 = "show tables"
    cur.execute(query1)
    
    tables = cur.fetchall()
    
    for table in tables:
    
        
        query = "select * from supermarket_sales"
        cur.execute(query)
    
    pandas_dataframe = pd.read_sql(query, connection)    
    # st.write(pandas_dataframe)
    AgGrid(pandas_dataframe)
    