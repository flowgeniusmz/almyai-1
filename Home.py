import streamlit as st
from config.data import get_data_salesforce_all
from config.sessionstate import initialize_session_state
from config.login import checkauthentication
from display.tileview import display_data

initialize_session_state()
if checkauthentication():
    

    dataOps, dataUsers, dataContracts = get_data_salesforce_all()

    display_data()

    tOpps, tUsers, tContracts = st.tabs(["Opportunities", "Users", "Contracts"])
    with tOpps:
        st.dataframe(dataOps)
    with tUsers:
        st.dataframe(dataUsers)
    with tContracts:
        st.dataframe(dataContracts)
