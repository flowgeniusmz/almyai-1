# home.py

import streamlit as st

#dfOpps = st.session_state.dfOpps

def chunk_dataframe(dataframe, chunk_size):
    for i in range(0, len(dataframe), chunk_size):
        yield dataframe.iloc[i:i + chunk_size]

def calculate_total_pages(dataframe, limit_per_page):
    totalpages = (len(dataframe) - 1) // limit_per_page + 1
    st.session_state.total_pages = totalpages
    return totalpages

def format_row_data(row):
    formatted_data = "<div>"
    for field in row._fields:
        if field not in ["Index", "attributes"]:  # Exclude specific fields
            value = getattr(row, field)
            if isinstance(value, dict) and 'Name' in value:
                value = value['Name']  # Extract 'Name' from nested objects
            elif isinstance(value, dict):
                continue  # Skip other complex nested objects
            formatted_data += f"<strong>{field.replace('_', ' ')}:</strong> {value}<br>"
    formatted_data += "</div>"
    return formatted_data

def display_data():
    calculate_total_pages(st.session_state.dfOpps, 12)
    st.session_state.currentpage = st.number_input("Page", min_value=1, max_value=st.session_state.total_pages, value=1, step=1)
    current_data = st.session_state.dfOpps.iloc[(st.session_state.currentpage - 1) * 12 : st.session_state.currentpage * 12]
    for chunk in chunk_dataframe(current_data, 3):
        cols = st.columns(3)
        for i, row in enumerate(chunk.itertuples()):
            with cols[i]:
                expander_title = f"Opportunity: {row.Name}\nExpiration Date: {row.CloseDate}\n90-Day Date: {row.CloseDate}"
                expander = st.expander(expander_title)
                with expander:
                    st.write(format_row_data(row), unsafe_allow_html=True)
        for i in range(len(chunk), 3):
            with cols[i]:
                st.empty()



