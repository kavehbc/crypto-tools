import streamlit as st
import hashlib
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def main():
    st.title("RSA Sign")
    private_key_file = st.file_uploader("Private Key", type=["pem"])
    data_file = st.file_uploader("Data File")

    if private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.getvalue(),
            password=None,
            backend=default_backend()
        )
    else:
        private_key = None

    if data_file:
        data_bytes = data_file.read()
        prehashed = hashlib.sha256(data_bytes).hexdigest()

        btn_sign = st.button("Sign")
        if btn_sign:
            sig = private_key.sign(
                bytes(prehashed.encode('ascii')),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())

            st.session_state.signature = base64.b64encode(sig)
            st.code(st.session_state.signature)

        if "signature" in st.session_state:
            if st.session_state.signature:
                st.download_button("Download Signature",
                                   data=st.session_state.signature,
                                   file_name="signature.sig")


if __name__ == '__main__':
    main()
