import streamlit as st
from st_supabase_connection import SupabaseConnection

def checkuser(username, password):
    qtable = "users"
    qttl = "10m"
    qcount = "exact"
    qcolumns = "*"
    qusernamecol = "Username"
    qpasswordcol = "Credential"

    # Set up the connection
    conn = st.connection("supabase", type=SupabaseConnection)

    # Perform the query
    response = conn.query(qcolumns, table=qtable, ttl=qttl, count=qcount).eq(qusernamecol, username).eq(qpasswordcol, password).execute()

    # Extract data and count from the response
    data = response.data
    count = response.count

    return data, count

def loginform():
    title = "Authentication"
    login_title = "Login to your account :prince:"
    login_username_label = "Enter your username (email)"
    login_username_placeholder = None
    login_username_help = None
    login_password_label = "Enter your password"
    login_password_placeholder = None
    login_password_help = None
    login_submit_label = "Login"
    login_success_message = "Login succeeded :tada:"
    login_error_message = "Wrong username/password :x:"

    exp_login = st.expander(title, expanded=not st.session_state.authenticated)
    with exp_login:
        tab_login, tab_help = st.tabs([login_title, "Help"])
        with tab_login:
            with st.form("login_form"):
                username = st.text_input(label = login_username_label, placeholder=login_username_placeholder, help=login_username_help, disabled=st.session_state.authenticated)
                password = st.text_input(label=login_password_label, placeholder=login_password_placeholder, help=login_password_help, disabled=st.session_state.authenticated, type="password")
                submit_button = st.form_submit_button(label=login_submit_label, disabled=st.session_state.authenticated, type="primary")
                if submit_button:
                    user_data, user_count = checkuser(username, password)
                    if user_count > 0:
                        st.session_state.authenticated = True
                        st.session_state.username = user_data[0]['Username']
                        st.session_state.credential = user_data[0]['Credential']
                        st.session_state.sfid = user_data[0]['Id']
                        st.session_state.firstname = user_data[0]['FirstName']
                        st.session_state.lastname = user_data[0]['LastName']
                        st.session_state.fullname = user_data[0]['Name']

                        # Display a welcome message
                        msg_success = st.success(login_success_message)
                    else:
                        msg_error = st.error(login_error_message)


def checkauthentication():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        loginform()
        return False
        
    if not st.session_state.authenticated:
        loginform()
        return False
    
    return True


