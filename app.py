import streamlit as st
import os
from services import database_connection
from view import (visualization,login,sidebar,
                  employee_dashboard,training_dashboard,
                  admin_level_client
)

# Set up Streamlit page
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                          "static/images/yash_logo.png")

st.set_page_config(page_title="YTMS", page_icon=image_path, 
                   layout="wide" ,initial_sidebar_state="collapsed")
st.image(image=image_path, width=135)
st.title("YTMS - Python Team")
# Hide developer features
# st.markdown(
#     """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Establish database connection
connection = database_connection.create_connection()

# Initialize session state for login, role, and page
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "Home"

if 'username' not in st.session_state: #add user_name and user_password for the keywords
    st.session_state.username = ""

if 'password' not in st.session_state:
    st.session_state.password = ""

# Login section
if not st.session_state.logged_in:
    #Make the user login
    login.user_login()

else:
    sidebar.create_sidebar()
    # Admin-specific file upload and download section

    if st.session_state.role == 'admin':
        # Ensure data folder exists
        data_path = "data"
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        #Add admin functionality to sidebar
        admin_level_client.show_admin_client(connection,data_path)

    # Display content based on page selection
    if st.session_state.page == "Home":
        #st.header("General Employee and Training Statistics")
        st.header(" ")
        visualization.show_general_visualizations()
        visualization.general_training_visualisation()

    elif st.session_state.page == "Employee Dashboard":

        employee_dashboard.display_employee_data(connection)

    elif st.session_state.page == "Training Dashboard":

        training_dashboard.display_training_data(connection)
