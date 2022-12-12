import streamlit as st
from cryptography.fernet import Fernet
import base64


def utf8(s: bytes):
    return str(s, 'utf-8')


def main():
    st.title("Fernet Encryption")
    key_option = st.radio("Key Option", options=["Manual", "Generate"], horizontal=True)
    if key_option == "Generate":
        key = Fernet.generate_key()
        st.code(utf8(key))
        st.button("Refresh Key")
    elif key_option == "Manual":
        secret = st.text_input("Secret", value="My secret")
        secret = bytes(secret.encode('ascii'))
        key = base64.b64encode(secret)
        st.code(utf8(key))
        st.caption("Key = Base64 Encoded Secret")
    data_file = st.file_uploader("Data File")
    if data_file:
        bytes_data = data_file.getvalue()
    else:
        bytes_data = None

    btn_encrypt = st.button("Encrypt")
    if btn_encrypt and bytes_data:
        f = Fernet(key)
        token = f.encrypt(bytes_data)
        # st.code(token)
        st.success("File encrypted successfully")
        st.download_button("Download Encrypted File",
                           data=token,
                           file_name=f"enc_{data_file.name}")

    btn_decrypt = st.button("Decrypt")
    if btn_decrypt and bytes_data:
        f = Fernet(key)
        token = f.decrypt(bytes_data)
        # st.code(token)
        st.success("File decrypted successfully")
        st.download_button("Download Decrypted File",
                           data=token,
                           file_name=f"dec_{data_file.name}")


if __name__ == '__main__':
    main()
