import string
from turtle import width
from numpy import identity
import streamlit as st
import base64
from superset import Superset
import json



def get_download_link(data, extension):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    b64 = base64.b64encode(data.encode('utf-8'))
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.{extension}">Download export    {extension}</a>' # decode b'abc' => abc



def main():
    ss = Superset()

    st.set_page_config(page_title="Data Visualize", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    st.sidebar.title("Controller")
    select = st.sidebar.selectbox('Option', ['Export Dashboard', 'Export Chart', 'Get Dashboard', 'Get Chart', 'Get Dataset'])

    if str(select).startswith("Export"):
        identify = st.sidebar.text_input("IDs")
        btn = st.sidebar.button("Export")
        if btn:
            if 'Dashboard' in str(select):
                data = ss.export_dashboard(int(identify)).text
                st.sidebar._html(get_download_link(data, 'yaml'))
            else:
                data = ss.export_chart(int(identify)).text
                st.sidebar._html(get_download_link(data, 'yaml'))
    elif str(select).startswith("Get"):
        identif= st.sidebar.text_input("IDs")
        btn = st.sidebar.button("Get")
        if btn:
            if 'Dashboard' in str(select):
                data = ss.get_dashboard(int(identif))
                data = json.dumps(data)
                st.sidebar._html(get_download_link(data, 'json'))
            elif 'Chart' in str(select):
                data = ss.get_chart(int(identif))
                data = json.dumps(data)
                st.sidebar._html(get_download_link(data, 'json'))   
            else:
                data = ss.get_dataset(int(identif))
                data = json.dumps(data)
                st.sidebar._html(get_download_link(data, 'json'))   



   
    st.components.v1.iframe("http://54.237.126.11:8088/superset/dashboard/p/RDVaoeGk9M7?standalone=1", width=1320, height=900, scrolling=True)



if __name__=='__main__':
    main();