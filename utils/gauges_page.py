import streamlit as st
from helpers.kuster_gauges_helper import Gauges_data_kuster
from PIL import Image
import os


package_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout="wide")

def gauges_kuster_page():
    """Read the data from kuster gauges over txt files and plot them.

    This function does not accept any parameters and excute
    a gauges data.
    """
    st.title("Down Hole Gauges _Kuster_ 🌡")
    st.markdown(
        """
        Quickly and easily manipulate the data from __Kuster__ Down Hole Memory Gauges \
        with our provided tool. View the data on the page or download it to Excel for \
            further analysis or processing.
                """
    )
    source_data_bottom = st.file_uploader(
        label="Uplaod bottom gauge data to web page", type=["csv", "txt"],
        key="file_bottom_unique"
    )
    st.write("---")
    try:
        # Execute the program
        Gauges_data_kuster(source_data_bottom)
    except Exception as e:
        st.write("An error occured:" + str(e))
