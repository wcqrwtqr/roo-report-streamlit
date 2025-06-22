import streamlit as st
from utils.intro import intro
from utils.sgs_tempate_geneator import generate_sgs_page
from utils.gauges_page import (
    # gauges_metrolog_page,
    # gauges_spartek_page,
    gauges_kuster_page,
)
from utils.plt_las import plt_las_page
from utils.md_tvd import md_tvd_page

if __name__ == "__main__":
    # Make the pages here in a Dict
    page_name_to_func = {
        "Intro Page": intro,
        "Gauges Kuster": gauges_kuster_page,
        "MD -> TVD": md_tvd_page,
        "PLT las": plt_las_page,
        # "Gauges Spartek": gauges_spartek_page,
        # "Gauges Metrolog": gauges_metrolog_page,
        "SGS Report": generate_sgs_page,
    }
    # Get the string of pages
    page_name = st.sidebar.selectbox("Choose page", page_name_to_func.keys())
    # make the pages
    page_name_to_func[page_name]()
