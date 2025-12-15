import mysql.connector
import streamlit as st
import pandas as pd


mysql_db = mysql.connector.connect(
    host="local host",
    user="root",
    password="root",
    database="crud"
)

# Testing the connection
if mysql_db.is_connected():
    st.success("MYSQL connection successfully established")
else:
    st.error("MYSQL connection failed")

mycursor = mysql_db.cursor()


def app():
    st.title("OPS Table – CRUD Operations")

    option = st.sidebar.selectbox(
        "SELECT THE OPERATION",
        ("ADD", "VIEW", "UPDATE", "DELETE", "FILTER")
    )

    # ADD
    if option == "ADD":
        st.subheader("Add New Order")

        name = st.text_input("Enter Name")
        product = st.text_input("Enter Product")
        qty = st.number_input("Enter Quantity", min_value=1)

        if st.button("ADD RECORD"):
            sql = "INSERT INTO ops (Name, Product, QTY) VALUES (%s, %s, %s)"
            value = (name, product, qty)
            mycursor.execute(sql, value)
            mysql_db.commit()
            st.success("Order added successfully")

    # VIEW
    elif option == "VIEW":
        st.subheader("View All Orders")

        mycursor.execute("SELECT * FROM ops")
        records = mycursor.fetchall()

        df = pd.DataFrame(records, columns=["orderID", "Name", "Product", "QTY"])
        st.dataframe(df)

    # UPDATE
    elif option == "UPDATE":
        st.subheader("Update Order")

        order_id = st.text_input("Enter Order ID")
        name = st.text_input("Enter New Name")
        product = st.text_input("Enter New Product")
        qty = st.number_input("Enter New Quantity", min_value=1)

        if st.button("UPDATE RECORD"):
            sql = """
                UPDATE ops 
                SET Name = %s, Product = %s, QTY = %s 
                WHERE orderID = %s
            """
            value = (name, product, qty, order_id)
            mycursor.execute(sql, value)
            mysql_db.commit()
            st.success("Order updated successfully")

    # DELETE
    elif option == "DELETE":
        st.subheader("Delete Order")

        order_id = st.text_input("Enter Order ID")

        if st.button("DELETE RECORD"):
            sql = "DELETE FROM ops WHERE orderID = %s"
            value = (order_id,)
            mycursor.execute(sql, value)
            mysql_db.commit()
            st.success("Order deleted successfully")

    # FILTER
    elif option == "FILTER":
        st.subheader("Filter Orders by Product")

        product = st.text_input("Enter Product Name")

        if st.button("FILTER"):
            sql = "SELECT * FROM ops WHERE Product LIKE %s"
            value = (f"%{product}%",)
            mycursor.execute(sql, value)
            records = mycursor.fetchall()

            if records:
                df = pd.DataFrame(records, columns=["orderID", "Name", "Product", "QTY"])
                st.dataframe(df)
            else:
                st.warning("No matching records found")

app()

