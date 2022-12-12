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

    key_file = st.file_uploader("Public/Private Key", type=["pem"])

    private_key = None
    if key_file:
        try:
            key = serialization.load_pem_private_key(
                key_file.getvalue(),
                password=None,
                backend=default_backend()
            )
            private_key = 1
        except:
            key = serialization.load_pem_public_key(
                key_file.getvalue(),
                backend=default_backend()
            )
            private_key = 0

    if private_key == 1:
        st.success("Private key is provided")
    elif private_key == 0:
        st.success("Public key is provided")

    plaintext = st.text_area("Data Content")
    bytes_data = str.encode(plaintext)

    if private_key == 0:
        btn_encrypt = st.button("Encrypt")
        st.caption("You can only encrypt data as large as the RSA key length.")
    if private_key == 1:
        btn_decrypt = st.button("Decrypt")

    if private_key == 0:
        if btn_encrypt:
            if key_file is None:
                st.error("Key is required")
            else:
                encrypted = base64.b64encode(key.encrypt(
                    bytes_data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ))
                st.code(f'{utf8(encrypted)}')

    if private_key == 1:
        if btn_decrypt:
            if key_file is None:
                st.error("Key is required")
            else:
                decrypted = key.decrypt(
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
