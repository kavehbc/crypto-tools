import streamlit as st
from apps import *


def main():

    pages = [
        st.Page(apps.home.home, title="Home", icon="🏠", default=True),
        st.Page(apps.jwt.jwt, title="JWT Tokenizer", icon="☕️"),
        st.Page(apps.generate_keys.generate_keys, title="Generate RSA Keys", icon="🔑"),
        st.Page(apps.encrypt.encrypt, title="RSA Encryption", icon="🔐"),
        st.Page(apps.sign.sign, title="RSA Sign", icon="🖋"),
        st.Page(apps.verifier.verifier, title="RSA Verify Signature", icon="🛃"),
        st.Page(apps.fernet.fernet, title="Fernet Encryption", icon="🔒"),
        st.Page(apps.hash.hash, title="Hash Encoder", icon="#⃣️"),
        st.Page(apps.base.base, title="Base64", icon="🔰"),
        st.Page(apps.otp.otp, title="One-Time Password", icon="🗝"),
        st.Page(apps.about.about, title="About Crypto Tools", icon="📖")
    ]

    pg = st.navigation(pages)
    pg.run()


if __name__ == '__main__':
    st.set_page_config(page_title="Crypto Toolbox",
                       page_icon="🔐",
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
    main()
