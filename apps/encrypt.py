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
    st.title("RSA Encrypt/Decrypt")

    private_key_file = st.file_uploader("Private Key", type=["pem"])
    public_key_file = st.file_uploader("Public Key", type=["pem"])

    if private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.getvalue(),
            password=None,
            backend=default_backend()
        )
    else:
        private_key = None

    if public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.getvalue(),
            backend=default_backend()
        )
    else:
        public_key = None

    plaintext = st.text_area("Data Content")
    bytes_data = str.encode(plaintext)

    btn_encrypt = st.button("Encrypt")
    st.caption("You can only encrypt data as large as the RSA key length.")

    if btn_encrypt:
        if public_key is None:
            st.error("Public Key is required to encrypt")
        else:
            encrypted = base64.b64encode(public_key.encrypt(
                bytes_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ))
            st.code(f'{utf8(encrypted)}')

    btn_decrypt = st.button("Decrypt")
    if btn_decrypt:
        if private_key is None:
            st.error("Private Key is required to encrypt")
        else:
            decrypted = private_key.decrypt(
                base64.b64decode(bytes_data),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            st.code(f'{utf8(decrypted)}')


if __name__ == '__main__':
    main()
