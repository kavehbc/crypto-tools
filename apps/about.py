import streamlit as st
import os
import inspect


def about():
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    markdown_file_path = parent_dir + "/README.md"
    license_file_path = parent_dir + "/LICENSE"

    if not os.path.exists(markdown_file_path):
        st.error("Markdown file does not exist.")
    else:
        with open(markdown_file_path, 'r', encoding="utf-8") as outfile:
            markdown_content = outfile.read()
        st.markdown(markdown_content, unsafe_allow_html=True)

    st.markdown("___")
    st.header("License")
    if not os.path.exists(license_file_path):
        st.error("License file does not exist.")
    else:
        with open(license_file_path, 'r', encoding="utf-8") as outfile:
            license_content = outfile.read()
        st.markdown(license_content, unsafe_allow_html=True)



if __name__ == '__main__':
    about()
