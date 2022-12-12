import streamlit as st
import hashlib
import base64
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def main():
    st.title("RSA Signature Verifier")
    public_key_file = st.file_uploader("Public Key", type=["pem"])
    signature_file = st.file_uploader("Signature File")
    data_file = st.file_uploader("Data File")

    if public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.getvalue(),
            backend=default_backend()
        )
    else:
        public_key = None

    prehashed = None
    if data_file:
        data_bytes = data_file.getvalue()
        prehashed = hashlib.sha256(data_bytes).hexdigest()

    signature = None
    if signature_file:
        base64_sig = signature_file.getvalue()
        signature = base64.b64decode(base64_sig)

    btn_verify = st.button("Verify")
    if btn_verify:
        if public_key is None:
            st.error("Public key is required")
        elif signature is None:
            st.error("Signature file is required")
        elif prehashed is None:
            st.error("Data file is required")
        else:
            try:
                public_key.verify(
                    signature,
                    bytes(prehashed.encode('ascii')),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256())
                st.success('Valid Signature')
            except InvalidSignature:
                st.error('Invalid Signature!')


if __name__ == '__main__':
    main()
