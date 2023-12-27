import streamlit as st

def initialize_session_state():

    if "username" not in st.session_state:
        st.session_state.username = ""
    if "credential" not in st.session_state:
        st.session_state.credential = ""
    if "sfid" not in st.session_state:
        st.session_state.sfid = ""
    if "firstname" not in st.session_state:
        st.session_state.firstname = ""
    if "lastname" not in st.session_state:
        st.session_state.lastname = ""
    if "fullname" not in st.session_state:
        st.session_state.fullname = ""
    if "currentpage" not in st.session_state:
        st.session_state.currentpage = 1
    if "totalpages" not in st.session_state:
        st.session_state.total_pages = 1
    if "dfOpps" not in st.session_state:
        st.session_state.dfOpps = None
    if "dfUsers" not in st.session_state:
        st.session_state.dfUsers = None
    if "dfContracts" not in st.session_state:
        st.session_state.dfContracts = None