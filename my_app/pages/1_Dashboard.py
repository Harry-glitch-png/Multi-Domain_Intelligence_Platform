import streamlit as st
import pandas as pd
import numpy as np
from app.data.db import connect_database
from app.data.incidents import *

st.set_page_config(page_title="Dashboard", page_icon="📊 ",
layout="wide")

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py") # back to the first page
    st.stop()

# Setup database
conn = connect_database()

# If logged in, show dashboard content
st.title("📊 Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# Example dashboard layout
st.caption("Welcome to the Multi-Domain Intelligence Platform")

# Allow category selections
categories = ["NONE","Cybersecurity", "Data Science", "IT Operations"]
selected_categories = st.selectbox("Select a domain:", categories)

st.write("You have selected:", selected_categories)

if selected_categories == "NONE":
    # Shows no data
    st.stop()

# ---------- Cybersecurity Display ----------
elif selected_categories == "Cybersecurity":

    st.subheader("Cyber Incidents by Category (Monthly):")

    col1, col2 = st.columns(2)
    # Group incidents by month and category
    chart_data = """
           SELECT strftime('%Y-%m', timestamp) as month, category, COUNT(*) as count
           FROM cyber_incidents
           GROUP BY month, category
           ORDER BY month
           """
    # Connects to database to run chart_data and to make a dataframe
    df = pd.read_sql_query(chart_data, conn)

    df_pivot = df.pivot(index="month", columns="category", values="count").fillna(0)

    # Show bar chart
    with col1:
        st.subheader("Line chart")
        st.line_chart(df_pivot)


    # Show the line chart
    with col2:
        st.subheader("\nBar chart")
        st.bar_chart(df_pivot)


    # Shows cyber_incidents data
    data = get_all_incidents(conn)
    with st.expander("See raw data"):
        st.dataframe(data)

    # Allow category selections
    edit_categories = ["Add", "Remove", "Update Status"]
    selected_categories = st.selectbox("Edit Cyber Incidents:", edit_categories)

    # Insert new incident
    if selected_categories == "Add":
        st.subheader("Add New Incident")
        with st.form("insert_form"):
            timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")
            severity = st.selectbox("Severity", ["Low", "Medium", "High"])
            category = st.selectbox("Category", ["DDos", "Malware", "Misconfiguration", "Phishing", "Unauthorized Access"])
            status = st.selectbox("Status", ["Open", "Investigating", "Closed"])
            description = st.text_area("Description")
            reported_by = st.text_input("Reported By (optional)")
            submitted = st.form_submit_button("Insert Incident")

            if submitted:
                incident_id = insert_incident(conn, timestamp, severity, category, status, description, reported_by)
                st.success(f"Incident {incident_id} inserted successfully!")

    # Remove incident
    elif selected_categories == "Remove":
        # Ensure state keys exist
        if "confirm_remove" not in st.session_state:
            st.session_state.confirm_remove = False
        if "incident_to_remove" not in st.session_state:
            st.session_state.incident_to_remove = ""

        st.subheader("Remove Incident")

        with st.form("remove_form"):
            incident_id = st.text_input("Incident ID")
            submitted = st.form_submit_button("Remove Incident")

            if submitted:
                # Move into confirmation mode and remember the ID
                st.session_state.confirm_remove = True
                st.session_state.incident_to_remove = incident_id

        if st.session_state.confirm_remove:
            st.warning(f"Are you sure you want to proceed?\nAll data of incident '{st.session_state.incident_to_remove}' will be permanently removed.")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Yes"):
                    st.success("Deleting incident...")
                    success = delete_incident(conn, st.session_state.incident_to_remove)
                    if success == 1:
                        st.success("Incident deletion successful!")
                    else:
                        st.warning("Incident deletion unsuccessful!")

                    # Reset state and clear input
                    st.session_state.confirm_remove = False
                    st.session_state.incident_to_remove = ""

            with col_b:
                if st.button("No"):
                    st.info("Action cancelled.")
                    # Reset state and clear input
                    st.session_state.confirm_remove = False
                    st.session_state.incident_to_remove = ""

    # Update incident
    elif selected_categories == "Update Status":
        st.subheader("Update Incident Status")
        with st.form("update_status"):
            incident_id = st.text_input("Incident ID")
            new_status = st.selectbox("Status", ["Open", "Investigating", "Closed"])
            submitted = st.form_submit_button("Update Incident")

            if submitted:
                update_incident_status(conn, incident_id, new_status)
                st.success(f"Incident {incident_id} updated successfully!")


# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")