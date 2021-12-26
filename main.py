import streamlit as st
from apps import *

lst_apps = {"home": "Home",
            "jwt": "JWT Tokenizer",
            "generate": "Generate RSA Keys",
            "encrypt": "RSA Encryption",
            "sign": "RSA Sign",
            "verify": "RSA Verify Signature",
            "fernet": "Fernet Encryption"}


def main():
    app = st.sidebar.selectbox("Menu", options=lst_apps.keys(),
                               format_func=lambda x: lst_apps[x])
    if app == "home":
        apps.home.main()
    if app == "jwt":
        apps.jwt.main()
    if app == "generate":
        apps.generate_keys.main()
    if app == "encrypt":
        apps.encrypt.main()
    if app == "sign":
        apps.sign.main()
    if app == "verify":
        apps.verifier.main()
    if app == "fernet":
        apps.fernet.main()


if __name__ == '__main__':
    main()
