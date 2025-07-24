import streamlit as st


def home():
    st.header("Welcome to Crypto Tools")
    st.write("""
        An Open-Source Toolbox for Daily Cryptography Needs
    """)
    st.info("Select one of the apps from the side bar menu")


if __name__ == '__main__':
    home()
