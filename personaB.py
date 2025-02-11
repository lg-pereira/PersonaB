# personaB.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Read Google Sheet as DataFrame")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(
    worksheet="Home",
    ttl="10m",
    usecols=[0, 5],
    nrows=1,
)

st.dataframe(df)
  
