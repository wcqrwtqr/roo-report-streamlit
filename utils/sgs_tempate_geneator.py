import streamlit as st
import os
from docx import Document

package_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout="wide")


def generate_sgs_page():
    """Take the input data and generate a final report \
    This is not final.
    """
    # st.title("Geneate the SGS report)
    st.title("ROO SGS Report Generator")
    st.markdown(
        """
        Generate the SGS final report for ROO operaiton \n
        Fill the fields to generate the final report quicly.
                """
    )
    st.write("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        unit_no = st.selectbox(
            "Unit Number", ["1", "2", "3"]
        )  # Or st.number_input for integers
        wellname = st.text_input("Well Name", "Ru-524")
        welltype = st.text_input("Well Type", "Production")
        fluid = st.text_input("Fluid", "Oil")
        min_res = st.text_input("Min Res", '3.44" no-go')
        spv = st.text_input("SPV", "Malik Mohamed")
    with col2:
        activity = st.text_input("Activity", "Daily, Pre and Post job WSD")
        activity_sgs = st.text_input("Activity SGS", "SGS")
        activity_dr = st.text_input("Activity DR", "DR")
        packer = st.text_input("Packer", "Packer")
        field = st.text_input("Field", "South Rumaila")
        sor = st.text_input("SOR", "34873")
    with col3:
        day = st.text_input("Day", "06")
        month = st.text_input("Month", "04")
        monthfull = st.text_input("Month (Full)", "April")
        year = st.text_input("Year", "2025")
        dgs = st.text_input("DGS", "MDS")
        tubing = st.text_input("Tubing", '4 1/2" 12.6# L-80')

    interval = st.text_input(
        "Interval",
        "3388, 3370, 3364, 3350, 3342, 3332, 3264, 2989, 1989, 989, 489, 0mGL",
    )

    if st.button("Generate Report"):
        # Define input and output paths
        # Corrected path handling
        template_file = f"utils/template{unit_no}.docx"
        # template_file = "utils/template1.docx"  # Corrected path handling
        output_file = f"{
            wellname}_NEOS_SGS_Final-Report_{year}{month}{day}.docx"

        # Ensure the template file exists
        if not os.path.exists(template_file):
            st.error(f"Template file not found: {template_file}")
        else:
            # Create the replacements dictionary
            replacements = {
                "{{well_name}}": wellname,
                "{{sor}}": sor,
                "{{date}}": f"{day}-{month}-{year}",
                "{{type}}": "Static Gradient Survey",
                "{{field}}": field,
                "{{dgs}}": dgs,
                "{{fluid}}": fluid,
                "{{packer}}": packer,
                "{{tubing}}": tubing,
                "{{welltype}}": welltype,
                "{{interval}}": interval,
                "{{min-res}}": min_res,
                "{{spv}}": spv,
            }

            try:
                replace_docx_variables(
                    template_file, output_file, replacements)
                st.success(f"Report generated successfully: {output_file}")

                # Offer download
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="Download Report",
                        data=file,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )

            except Exception as e:
                # Display the error message
                st.error(f"An error occurred: {e}")


def replace_docx_variables(input_file, output_file, replacements):
    """Replace variables in DOCX file, including headers and footers, using python-docx."""
    document = Document(input_file)

    # Helper function to replace text in a paragraph or cell
    def replace_text(element):
        if element:
            for key, value in replacements.items():
                if key in element.text:
                    element.text = element.text.replace(key, str(value))

    # Replace in paragraphs and tables in the main document
    for paragraph in document.paragraphs:
        replace_text(paragraph)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                replace_text(cell)

    # Replace in headers
    for section in document.sections:
        header = section.header
        if header:
            for paragraph in header.paragraphs:
                replace_text(paragraph)
            for table in header.tables:
                for row in table.rows:
                    for cell in row.cells:
                        replace_text(cell)

    # Replace in footers
    for section in document.sections:
        footer = section.footer
        if footer:
            for paragraph in footer.paragraphs:
                replace_text(paragraph)
            for table in footer.tables:
                for row in table.rows:
                    for cell in row.cells:
                        replace_text(cell)

    document.save(output_file)
