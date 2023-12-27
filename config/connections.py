import streamlit as st
from simple_salesforce import Salesforce
from st_supabase_connection import SupabaseConnection

@st.cache_resource
def get_supabase():
    conn = st.connection("supabase", type=SupabaseConnection)
    return conn

@st.cache_resource
def get_salesforce():
    sf = Salesforce(username=st.secrets.salesforce.sfuser, password=st.secrets.salesforce.sfcred, security_token=st.secrets.salesforce.sftoken)
    return sf