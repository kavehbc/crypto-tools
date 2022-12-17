import streamlit as st
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def utf8(s: bytes):
    return str(s, 'utf-8')


def main():
    st.title("Generate RSA Keys")
    key_size_options = [128, 256, 1024, 2048, 4096, 8192]
    key_size = int(st.selectbox("Key Size (bit)", options=key_size_options, index=len(key_size_options) - 1))
    st.caption(f"RSA can encrypt up to key size bits minus OAEP Padding (42) bytes")
    st.caption(f"{key_size}-bit RSA can encrypt up to {(key_size / 8) - 42:,.0f} bytes")
    btn_generate = st.button("Generate Keys")

    if btn_generate:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        st.session_state['private_pem'] = private_pem

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        st.session_state['public_pem'] = public_pem

    if 'public_pem' in st.session_state:
        private_pem = st.session_state['private_pem']
        public_pem = st.session_state['public_pem']

        with st.expander("Private Key"):
            st.code(private_pem.decode("utf-8"))
        with st.expander("Public Key"):
            st.code(public_pem.decode("utf-8"))

        st.download_button("Download Private Key",
                           data=private_pem,
                           file_name="private_key.pem",
                           mime="application/x-pem-file")
        st.download_button("Download Public Key",
                           data=public_pem,
                           file_name="public_key.pem",
                           mime="application/x-pem-file")


if __name__ == '__main__':
    main()
