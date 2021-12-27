import streamlit as st
from apps import *

lst_apps = {"home": "Home",
            "jwt": "JWT Tokenizer",
            "generate": "Generate RSA Keys",
            "encrypt": "RSA Encryption",
            "sign": "RSA Sign",
            "verify": "RSA Verify Signature",
            "fernet": "Fernet Encryption",
            "base64": "Base64 Encoder/Decoder",
            "about": "About Crypto Tools"}


def main():
    st.set_page_config(page_title="Crypto Toolbox",
                       page_icon=None,
                       layout="centered",
                       initial_sidebar_state="auto",
                       menu_items={
                           'Get Help': 'https://github.com/kavehbc/crypto-tools',
                           'Report a bug': "https://github.com/kavehbc/crypto-tools/issues",
                           'About': """
                               # Crypto Toolbox
                               
                               Handy tools for your daily cryptography needs
                           """
                       })

    app = st.sidebar.selectbox("Menu", options=lst_apps.keys(),
                               format_func=lambda x: lst_apps[x])
    if app == "home":
        apps.home.main()
    if app == "about":
        apps.about.main()

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
    if app == "base64":
        apps.base.main()


if __name__ == '__main__':
    main()
