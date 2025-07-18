import streamlit as st
import os
from PIL import Image


def intro():
    st.title("NEOS Webkit Application")
    st.title("Oil field tool kit")
    st.subheader("👈🏼 Select service from menu bar")
    st.subheader("About the web site:")
    st.markdown(
        """
                    This website is ment to be used for generating SGS report and graphing Dowh Hole Memory gauges used for ROO operation and easy of exporting Final reports for our clinet.\n
                    You can generate graphs and adjust it to the duration you desire and calculate the average values of the selected fields
                    then download it to csv.\n
                    Done by": Mohammed Salah Albatati.\n
                    """
    )
    st.write("---")
    # st.write(
    #     "Feel free to follow me in my YouTube channel for more video on data processing"
    # )

    # Get the absolute path of the current directory
    package_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the thumbnail image using os.path.join
    image_path = os.path.join(package_dir, "..", "Thumbnail", "IMG_9889.JPG")

    # Open the image
    try:
        image = Image.open(image_path)
        st.image(image, caption="Free Palestine")
    except FileNotFoundError:
        st.error("Image not found at path: " + image_path)
